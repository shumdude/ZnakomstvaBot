from config import Config, load_config

LEXICON: dict[str, str] = {"start": "Приветствую! Я - бот знакомств (16+)\n\n"
                                    "Чтобы создать анкету, воспользуйтесь командой /registration",
                           "registration": "Для начала введи свой возраст (не менее 16 лет):\n\n"
                                           "Для того, чтобы отменить регистрацию, воспользуйтесь командой /cancel",
                           "registration_ok": "Вы зарегистрированы!\n\n"
                                              "Для просмотра чужих анкет нажмите кнопку ниже",
                           "not_16": "Вам нет 16 лет. Отклоняем анкету.\n\n"
                                     "Для повторной регистрации воспользуйтесь командой /registration",
                           "registration_yet": "Вы уже зарегистрированы",
                           "my_info": "Моя анкета",
                           "next": "Смотреть следующую анкету",
                           "start_search": "Начать поиск анкет"}

config: Config = load_config('.env')
TORTOISE_ORM = {
    'connections': {'default': f"asyncpg://"
                               f"{config.db.db_user}:"
                               f"{config.db.db_password}@"
                               f"{config.db.db_host}:"
                               f"{config.db.db_port}/"
                               f"{config.db.database}"},
    'apps': {
        'app': {
            'models': ['database.models', 'aerich.models'],
            'default_connection': 'default'
        },
    },
}
