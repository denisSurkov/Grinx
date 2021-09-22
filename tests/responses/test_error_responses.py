from responses.errors import NotFoundResponse


def test_not_found_response_sets_correct_fields():
    response = NotFoundResponse()

    assert response.status_code == 404
    assert response.status_message == 'Not Found'
