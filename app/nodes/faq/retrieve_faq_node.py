from app.models.state import State
from app.services.faq_service import get_faq_service


def retrieve_faq(state: State):
    try:

        faq_service = get_faq_service()
        results = faq_service.search_faq(state["question"])

        print("faq_results: ", results)

        return {"faq_results": results}
    except Exception as e:
        print(f"Error in retrieve_faq: {e}")
        return {"faq_results": []}
