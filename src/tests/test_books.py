book_prefix = "/api/v1/books/"
def test_get_all_books(test_client,fake_book_service,fake_session):
    response = test_client.get(
        url=f"{book_prefix}"
    )
    assert fake_book_service.get_all_books_called_once()
    assert fake_book_service.get_all_books_called_once_with(fake_session)