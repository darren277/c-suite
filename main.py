import re
import openai
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from settings import GPT_MODEL, OPENAI_API_KEY, PERSONAS, SLACK_BOT_TOKEN, SLACK_APP_TOKEN

# --- Initialization ---
app = App(token=SLACK_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY


# --- Placeholder for your RAG logic ---
def retrieve_from_knowledge_base(query: str) -> str:
    """
    Searches your knowledge base (e.g., a vector database) and returns relevant context.
    """
    print(f"Searching knowledge base for: {query}")
    # In a real app, this would query something like Pinecone, ChromaDB, etc.
    # For now, we'll return some dummy context.
    if "hiring" in query.lower():
        return "Context: The Q4 hiring plan prioritizes two senior backend engineers and one product marketing manager. Budget has been approved."
    return "Context: No specific information found on that topic."

# --- Slack Event Listener ---
@app.event("app_mention")
def handle_app_mention_events(body, client, say, logger):
    event = body['event']
    channel_id = event['channel']
    thread_ts = event.get('thread_ts', event['ts'])
    user_query = event['text']
    
    # 1. Identify which bot was mentioned
    mentioned_users = re.findall(r"<@(\w+)>", user_query)
    if not mentioned_users:
        return # Should not happen in an app_mention event
    
    bot_user_id = mentioned_users[0]
    persona = PERSONAS.get(bot_user_id)
    
    if not persona:
        logger.warning(f"Mentioned user {bot_user_id} not found in PERSONAS.")
        return

    # Clean the user query to remove the @mention
    clean_query = user_query.replace(f"<@{bot_user_id}>", "").strip()

    try:
        # Give a visual cue that the bot is thinking
        thinking_message = say(text=f"Thinking as the {persona['name']}...", thread_ts=thread_ts)

        # 2. Retrieve context with your RAG mechanism
        rag_context = retrieve_from_knowledge_base(clean_query)

        # 3. Fetch conversation history
        history = client.conversations_history(channel=channel_id, limit=5)
        conversation_history = [msg['text'] for msg in reversed(history['messages'])]

        # 4. Build the prompt and call the OpenAI API
        messages_for_api = [
            {"role": "system", "content": persona['system_prompt']},
            {"role": "user", "content": f"""
            Here is the recent conversation history:
            ---
            {"\n".join(conversation_history)}
            ---
            
            Here is some internal knowledge that might be relevant:
            ---
            {rag_context}
            ---

            Based on all of this, please answer my latest question: "{clean_query}"
            """}
        ]
        
        response = openai.chat.completions.create(
            model=GPT_MODEL,
            messages=messages_for_api
        )
        api_response = response.choices[0].message.content

        # Update the "Thinking..." message with the final answer
        client.chat_update(
            channel=channel_id,
            ts=thinking_message['ts'],
            text=api_response
        )

    except Exception as e:
        logger.error(f"Error handling app_mention: {e}")
        client.chat_update(
            channel=channel_id,
            ts=thinking_message['ts'], # Fails if thinking_message wasn't posted
            text="Sorry, I ran into an error!"
        )

# --- Start the App ---
if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
