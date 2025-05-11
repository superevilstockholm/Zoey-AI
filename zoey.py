import aiohttp

import os
from dotenv import load_dotenv

from typing import Literal

class Core:
    def __init__(self):
        load_dotenv()
        self.GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
        self.OPEN_ROUTER_API_KEY = os.environ.get("OPEN_ROUTER_API_KEY")
        self.custom_instruction = open("custom_instruction.txt", "r").read()
        self.session = None

    async def __create_session(self):
        await self.close_session()
        self.session = aiohttp.ClientSession()

    async def close_session(self):
        if self.session and not self.session.closed:
            await self.session.close()

    async def __gemini(self, prompt: str, session: aiohttp.ClientSession, model: str = "gemini-2.0-flash", retry: int = 3) -> dict:
        if retry == 0: return {"status": False, "message": "Gagal mendapatkan response setelah 3 kali percobaan.", "response": None}
        try:
            async with session.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={self.GEMINI_API_KEY}",
                headers={"User-Agent": "Gemini Agent (python v3.12.2; aiohttp; asyncio)", "Content-Type": "application/json"},
                json={
                    "systemInstruction": {
                        "role": "system",
                        "parts": [
                            {
                                "text": self.custom_instruction
                            }
                        ]
                    },
                    "contents": [
                        {
                            "role": "user",
                            "parts": [
                                {
                                    "text": f"{prompt}"
                                }
                            ]
                        }
                    ],
                    "safetySettings": [
                        {
                            "category": "HARM_CATEGORY_HATE_SPEECH",
                            "threshold": "BLOCK_NONE"
                        },
                        {
                            "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                            "threshold": "BLOCK_NONE"
                        },
                        {
                            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                            "threshold": "BLOCK_NONE"
                        },
                        {
                            "category": "HARM_CATEGORY_HARASSMENT",
                            "threshold": "BLOCK_NONE"
                        }
                    ]
                }
            ) as response:
                if response.status == 200:
                    return {"status": True, "message": None, "response": await response.json()}
                else:
                    return {"status": False, "message": await response.text(), "response": None}
        except Exception as e:
            print(f"Terjadi kesalahan, error: {e}. Retrying... {retry - 1} percobaan tersisa")
            return await self.__gemini(prompt, session, model, retry - 1)

    async def generate_response(self, prompt: str, model: Literal["gemini"] = "gemini") -> dict:
        if not self.session or self.session.closed:
            await self.__create_session()
        if model == "gemini":
            return await self.__gemini(prompt, self.session)
        else:   
            return {"status": False, "message": "Model tidak ditemukan.", "response": None}