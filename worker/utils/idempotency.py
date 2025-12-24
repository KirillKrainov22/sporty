from worker.repositories.event_repo import is_processed, mark_processed


async def check_and_mark(session, event_id: str) -> bool:
    """
    True  -> событие уже обработано, ничего не делаем
    False -> можно обрабатывать
    """
    if await is_processed(session, event_id):
        return True

    await mark_processed(session, event_id)
    return False