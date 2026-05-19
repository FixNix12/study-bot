from aiogram.fsm.state import State, StatesGroup


class AskAiState(StatesGroup):
    waiting_for_question = State()