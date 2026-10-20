"""Minimal Amazon Bedrock helper; disabled by default."""
import os

SYSTEM_PROMPT = (
    "You are an IT service desk assistant. Give concise, safe guidance. Do not claim access to company systems. "
    "Never ask for passwords, MFA codes, recovery keys, or secrets. Never invent company policies or internal URLs. "
    "If policy is unknown, say so and recommend contacting IT support. Do not suggest destructive changes or "
    "bypassing security controls."
)

def answer_it_question(question: str) -> str:
    if os.getenv("BEDROCK_ENABLED", "false").lower() != "true":
        return ("The AI knowledge feature is currently disabled. I can help with standard VPN, Outlook, "
                "account-access, and software-installation workflows. Contact IT for organization-specific guidance.")
    model_id = os.getenv("BEDROCK_MODEL_ID", "").strip()
    if not model_id:
        raise RuntimeError("BEDROCK_MODEL_ID must be configured when BEDROCK_ENABLED=true")
    import boto3
    client = boto3.client("bedrock-runtime", region_name=os.getenv("AWS_REGION"))
    response = client.converse(
        modelId=model_id,
        system=[{"text": SYSTEM_PROMPT}],
        messages=[{"role": "user", "content": [{"text": (question or "")[:3000]}]}],
        inferenceConfig={"maxTokens": 350, "temperature": 0.2, "topP": 0.8},
    )
    blocks = response.get("output", {}).get("message", {}).get("content", [])
    answer = " ".join(b.get("text", "") for b in blocks if b.get("text"))
    return answer[:3000] if answer.strip() else "I couldn't generate a reliable answer. Please contact IT support."

