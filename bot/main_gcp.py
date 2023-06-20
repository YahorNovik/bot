import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.storage.redis import RedisStorage, Redis
from commands import add_payment, exit_button, logon, open_gabinet, invoice, add_gabinet, dummy_message

async def main():

  # lekarz dentysta
  API_TOKEN: str = '5888769925:AAGNCIsmXjoP9Kj-AtWKtW0s9iiu7CaTBLM'    
  # B2B Developer
  #API_TOKEN: str = '6030957150:AAGkocaEhNBlG9Ge0PkAPwMe3i4S0iAPEMo'
  storage: MemoryStorage = MemoryStorage()  
  #redis: Redis = Redis(host='localhost')
  #storage: RedisStorage = RedisStorage(redis=redis)

  #config: Config = load_config()
  #bot: Bot = Bot(token=config.tg_bot.token)
  
  bot: Bot = Bot(token=API_TOKEN)
  dp: Dispatcher = Dispatcher(bot=bot, storage=storage)

  dp.include_router(exit_button.router)  
  dp.include_router(logon.router)
  dp.include_router(add_payment.router)
  dp.include_router(add_gabinet.router)
  dp.include_router(open_gabinet.router)
  dp.include_router(invoice.router)
  dp.include_router(dummy_message.router)

  await bot.delete_webhook(drop_pending_updates=True)
  await dp.start_polling(bot)
  

if __name__ == '__main__':
    print('started....')
    asyncio.run(main())

  

    