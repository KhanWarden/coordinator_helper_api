from typing import Optional, Tuple
from datetime import date, datetime, timedelta, time

import pytz
import aiohttp
from aiohttp import web

from src.core.config import settings
from src.schemas.schedule.erp_user import ErpUserSchema

LOGIN_URL: str = "https://api.plus-erp.app/api/core/v2/user/signin"


class ErpCrawler:
    async def get_schedule(self, date_: date | None = None) -> dict:
        async with aiohttp.ClientSession() as session:

            erp_user_headers = await self._get_erp_user_headers(session)
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {erp_user_headers.token}",
                "CabinetId": str(erp_user_headers.cabinet_id),
            }
            day_before_date, day_date = self._get_date(date_)
            town_time = self._get_town_utc("Almaty")
            api_endpoint = (
                f"https://api.plus-erp.app/api/sales/order?catalog_id=&show_deleted=false&"
                f"start_time={day_before_date}T{town_time}&end_time={day_date}T{town_time}&size=-1"
            )

            async with session.get(api_endpoint, headers=headers) as api_response:
                if api_response.status != 200:
                    raise web.HTTPUnauthorized(text="Invalid credentials")
                schedule = await api_response.json()
                return schedule

    @staticmethod
    def _get_town_utc(city: str) -> str:
        user_tz = pytz.timezone(f"Asia/{city}")
        now = datetime.now(user_tz)
        offset_hours = int(now.utcoffset().total_seconds() // 3600)

        adjusted_hour = 24 - offset_hours

        t = time(adjusted_hour, 0, 0)
        return t.strftime("%H:%M:%S")

    @staticmethod
    def _get_date(date_: date | None) -> Tuple[str, str]:
        if not date_:
            today = datetime.today()
            yesterday = today - timedelta(days=1)
            return yesterday.strftime("%Y-%m-%d"), today.strftime("%Y-%m-%d")
        current_date = date_
        day_before_date = current_date - timedelta(days=1)
        return day_before_date.strftime("%Y-%m-%d"), current_date.strftime("%Y-%m-%d")

    async def _get_erp_user_headers(
        self, session: aiohttp.ClientSession
    ) -> ErpUserSchema:
        credentials = {
            "email": settings.PLUS_ERP_LOGIN,
            "password": settings.PLUS_ERP_PASSWORD,
        }

        async with session.post(
            LOGIN_URL, json=credentials, headers={"Content-Type": "application/json"}
        ) as login_resp:
            if login_resp.status != 200:
                raise web.HTTPUnauthorized(text="Invalid credentials")
            login_data = await login_resp.json()

            user_headers = ErpUserSchema(
                token=login_data.get("accessToken"),
                cabinet_id=int(login_data.get("cabinet").get("id")),
            )
            return user_headers
