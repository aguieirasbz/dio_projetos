from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
from ultils.Config import Config

def analyze_credit_card(card_url):
    # Configurar as credenciais e cliente
    credential = AzureKeyCredential(Config.KEY)
    document_client = DocumentIntelligenceClient(Config.ENDPOINT, credential)
    # Analisar o documento com o modelo pré-construído "creditCard"
    card_info = document_client.begin_analyze_document(
        "prebuilt-creditCard", AnalyzeDocumentRequest(url_source=card_url))
    result = card_info.result()

    # Extrair campos relevantes do resultado
    for document in result.documents:
        fields = document.get("fields", {})
        return {
            "card_name": fields.get("CardHolderName", {}).get("content"),
            "card_number": fields.get("CardNumber", {}).get("content"),
            "expiry_date": fields.get("ExpirationDate", {}).get("content"),
            "bank_name": fields.get("IssuingBank", {}).get("content"),
        }
