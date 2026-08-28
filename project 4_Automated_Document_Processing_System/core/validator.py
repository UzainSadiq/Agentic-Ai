from schemas.document_schema import DocumentResult


def validate_result(data: dict):
    try:
        result = DocumentResult.model_validate(data)
        return True, result, None
    except Exception as exc:
        return False, None, str(exc)
