"""Response templates for email categories.

This module contains predefined response templates for different email categories
in multiple languages. Templates are used both for few-shot learning examples
and as fallback responses when LLM generation fails.

Categories:
- payment_issue: Billing, invoicing, payment processing problems
- technical_support: Software bugs, crashes, technical difficulties
- information_request: Questions about features, pricing, or general info
- greeting: Casual messages, holiday wishes, informal communication
- complaint: Customer dissatisfaction, negative feedback
- spam: Promotional content, irrelevant messages
"""

RESPONSE_TEMPLATES = {
    "pt": {
        "payment_issue": {
            "subject": "Re: Problema com Pagamento - Equipe Financeira",
            "body": (
                "Prezado(a) cliente,\n\n"
                "Recebemos sua solicitação referente ao problema com pagamento. "
                "Nossa equipe financeira já está analisando seu caso e trabalhando para resolver a situação o mais rápido possível. "
                "Entendemos a importância dessa questão e daremos prioridade ao seu atendimento.\n\n"
                "Um especialista da área financeira entrará em contato em até 24 horas com uma solução "
                "ou com os próximos passos necessários para regularizar a situação.\n\n"
                "Agradecemos pela compreensão e paciência.\n\n"
                "Atenciosamente,\n"
                "Equipe de Suporte Financeiro"
            )
        },
        "technical_support": {
            "subject": "Re: Suporte Técnico - Análise em Andamento",
            "body": (
                "Prezado(a) cliente,\n\n"
                "Obrigado por reportar o problema técnico. Nossa equipe de engenharia já iniciou "
                "a investigação detalhada do caso que você descreveu. Compreendemos como isso pode impactar "
                "sua experiência com nosso produto.\n\n"
                "Estamos trabalhando para identificar a causa raiz e implementar uma solução. "
                "Você receberá atualizações sobre o progresso e, assim que resolvermos, "
                "entraremos em contato imediatamente.\n\n"
                "Enquanto isso, se tiver informações adicionais que possam nos ajudar, "
                "fique à vontade para responder este email.\n\n"
                "Atenciosamente,\n"
                "Equipe de Suporte Técnico"
            )
        },
        "information_request": {
            "subject": "Re: Sua Solicitação de Informações",
            "body": (
                "Olá,\n\n"
                "Obrigado pelo seu interesse! Recebemos sua solicitação de informações "
                "e teremos prazer em ajudá-lo com os detalhes que precisa.\n\n"
                "Nossa equipe de atendimento está preparando uma resposta completa e detalhada "
                "para sua pergunta. Você receberá todas as informações solicitadas em breve, "
                "junto com materiais adicionais que podem ser úteis.\n\n"
                "Se tiver outras dúvidas enquanto isso, não hesite em nos contatar.\n\n"
                "Atenciosamente,\n"
                "Equipe de Atendimento ao Cliente"
            )
        },
        "greeting": {
            "subject": "Re: Sua Mensagem",
            "body": (
                "Olá,\n\n"
                "Agradecemos muito pelo seu contato e pelas palavras gentis! "
                "É sempre um prazer ouvir de nossos clientes.\n\n"
                "Desejamos tudo de melhor para você também!\n\n"
                "Atenciosamente,\n"
                "Equipe de Suporte"
            )
        },
        "complaint": {
            "subject": "Re: Seu Feedback - Prioridade Alta",
            "body": (
                "Prezado(a) cliente,\n\n"
                "Lamentamos profundamente pela experiência negativa que você teve. "
                "Seu feedback é extremamente importante para nós e levamos todas as reclamações muito a sério.\n\n"
                "Sua situação foi encaminhada para nossa gerência com prioridade alta. "
                "Estamos comprometidos em resolver este problema e garantir que sua experiência melhore significativamente. "
                "Um supervisor entrará em contato pessoalmente em até 12 horas para discutir uma solução adequada.\n\n"
                "Agradecemos pela oportunidade de corrigir a situação.\n\n"
                "Atenciosamente,\n"
                "Gerência de Atendimento ao Cliente"
            )
        },
        "spam": {
            "subject": "Re: Mensagem Recebida",
            "body": (
                "Olá,\n\n"
                "Agradecemos pelo contato.\n\n"
                "Atenciosamente,\n"
                "Equipe de Suporte"
            )
        }
    },
    "en": {
        "payment_issue": {
            "subject": "Re: Payment Issue - Financial Team",
            "body": (
                "Dear customer,\n\n"
                "We have received your request regarding the payment issue. "
                "Our financial team is already analyzing your case and working to resolve the situation as quickly as possible. "
                "We understand the importance of this matter and will prioritize your service.\n\n"
                "A specialist from the financial department will contact you within 24 hours with a solution "
                "or with the next steps needed to regularize the situation.\n\n"
                "Thank you for your understanding and patience.\n\n"
                "Best regards,\n"
                "Financial Support Team"
            )
        },
        "technical_support": {
            "subject": "Re: Technical Support - Analysis in Progress",
            "body": (
                "Dear customer,\n\n"
                "Thank you for reporting the technical issue. Our engineering team has already started "
                "a detailed investigation of the case you described. We understand how this may impact "
                "your experience with our product.\n\n"
                "We are working to identify the root cause and implement a solution. "
                "You will receive updates on the progress, and as soon as we resolve it, "
                "we will contact you immediately.\n\n"
                "In the meantime, if you have any additional information that could help us, "
                "feel free to reply to this email.\n\n"
                "Best regards,\n"
                "Technical Support Team"
            )
        },
        "information_request": {
            "subject": "Re: Your Information Request",
            "body": (
                "Hello,\n\n"
                "Thank you for your interest! We have received your information request "
                "and will be happy to help you with the details you need.\n\n"
                "Our customer service team is preparing a complete and detailed response "
                "to your question. You will receive all the requested information shortly, "
                "along with additional materials that may be useful.\n\n"
                "If you have other questions in the meantime, don't hesitate to contact us.\n\n"
                "Best regards,\n"
                "Customer Service Team"
            )
        },
        "greeting": {
            "subject": "Re: Your Message",
            "body": (
                "Hello,\n\n"
                "We really appreciate your contact and kind words! "
                "It's always a pleasure to hear from our customers.\n\n"
                "We wish you all the best as well!\n\n"
                "Best regards,\n"
                "Support Team"
            )
        },
        "complaint": {
            "subject": "Re: Your Feedback - High Priority",
            "body": (
                "Dear customer,\n\n"
                "We deeply regret the negative experience you had. "
                "Your feedback is extremely important to us and we take all complaints very seriously.\n\n"
                "Your situation has been escalated to our management with high priority. "
                "We are committed to resolving this issue and ensuring your experience improves significantly. "
                "A supervisor will personally contact you within 12 hours to discuss an appropriate solution.\n\n"
                "Thank you for the opportunity to make this right.\n\n"
                "Best regards,\n"
                "Customer Service Management"
            )
        },
        "spam": {
            "subject": "Re: Message Received",
            "body": (
                "Hello,\n\n"
                "Thank you for reaching out.\n\n"
                "Best regards,\n"
                "Support Team"
            )
        }
    }
}

# Category descriptions for documentation and prompt engineering
CATEGORY_DESCRIPTIONS = {
    "payment_issue": {
        "description": "Issues related to billing, invoicing, payment processing, or financial transactions",
        "examples": ["can't pay invoice", "billing error", "charge on my card", "refund request"]
    },
    "technical_support": {
        "description": "Software bugs, crashes, errors, performance issues, or technical difficulties",
        "examples": ["app crashes", "error message", "cannot login", "feature not working"]
    },
    "information_request": {
        "description": "Questions about features, pricing, documentation, or general information",
        "examples": ["how does it work", "pricing question", "feature availability", "documentation"]
    },
    "greeting": {
        "description": "Casual messages, holiday wishes, informal communication, or social interaction",
        "examples": ["happy holidays", "thank you", "great job", "just saying hi"]
    },
    "complaint": {
        "description": "Customer dissatisfaction, negative feedback, frustration, or service quality issues",
        "examples": ["unhappy with service", "disappointed", "this is unacceptable", "poor quality"]
    },
    "spam": {
        "description": "Promotional content, irrelevant messages, or unsolicited communication",
        "examples": ["buy now", "click here for discount", "you've won", "unrelated marketing"]
    }
}

def get_template(language: str, category: str) -> dict:
    """Get a response template for a specific language and category.

    Args:
        language (str): Language code ('pt' or 'en').
        category (str): Email category (payment_issue, technical_support, etc.).

    Returns:
        dict: Template with 'subject' and 'body' keys.

    Raises:
        KeyError: If language or category is not found.
    """
    return RESPONSE_TEMPLATES[language][category]

def get_all_categories() -> list:
    """Get list of all available email categories.

    Returns:
        list: List of category keys.
    """
    return list(CATEGORY_DESCRIPTIONS.keys())

def get_category_description(category: str) -> dict:
    """Get description and examples for a specific category.

    Args:
        category (str): Email category.

    Returns:
        dict: Description and examples for the category.
    """
    return CATEGORY_DESCRIPTIONS[category]
