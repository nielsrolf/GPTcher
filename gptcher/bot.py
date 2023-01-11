"""
We have a conversation flow that is defined by the states of the conversation.
For each message, the user is loaded from the database, and the state of the conversation is loaded.
The message is passed to the state, and the state responds to the message.
While doing so, it can update the user or conversation state.

Messages are connected to a session via the session ID.
"""
from gptcher.main import STATES, ExerciseSelectState, supabase, ConversationState
from gptcher.vocabulary import Vocabulary


# @measure_time
async def respond(user_id, message, reply_func):
    """Respond to a message from a user.

    Loads the user history and the conversation state, and passes the message to the state.

    Args:
        user_id: The ID of the user.
        message: The message sent by the user.

    Returns:
        A response to the message.
    """
    user_id = str(user_id) + "tmp4"
    user = User(user_id, reply_func=reply_func)
    await user.state.respond(message)


async def start_exercise(user_id, reply_func):
    """Start an exercise.

    Args:
        user_id: The ID of the user.
    """
    user_id = str(user_id) + "tmp4"
    user = User(user_id, reply_func=reply_func)
    new_conversation = ExerciseSelectState(
        user,
    )
    await user.enter_state(new_conversation)


async def change_language(user_id, language, reply_func):
    user_id = str(user_id) + "tmp4"
    user = User(user_id, reply_func=reply_func)
    await user.change_language(language)


class User:
    """A user of the bot.

    If the user is new, the user is created with the default state.
    If the user already exists, the user is loaded from the database.
    """

    def __init__(self, user_id, reply_func):
        self.user_id = user_id
        self.reply = reply_func
        self.language = None
        self.state = None
        self.vocabulary = None
        self._load_state()
    
    async def change_language(self, language):
        self.language = language
        supabase.table("users").update({"language": language}).eq("user_id", self.user_id).execute()
        self.vocabulary = Vocabulary(self, language)
        new_conversation = ConversationState(self)
        await self.enter_state(new_conversation)

    def _load_state(self):
        """Load the state of the user from the database.

        If the user is new, the default state is returned.
        """
        user_db = (
            supabase.table("users").upsert({"user_id": self.user_id}).execute().data[0]
        )
        print("session", user_db["session"])
        self.language = user_db["language"]
        # Get the session from the database or create a new one if the user is new
        is_new_user = user_db["session"] is None
        if is_new_user:
            session_response = (
                supabase.table("session").insert({"user_id": self.user_id}).execute()
            )
        else:
            session_response = (
                supabase.table("session")
                .select("*")
                .eq("id", user_db["session"])
                .execute()
            )
        session = session_response.data[0]
        self.vocabulary = Vocabulary.from_list(self, user_db["words"])
        try:
            self.state = STATES[session["type"]](self, session["id"], session["context"])
        except:
            self.enter_state(ConversationState(self))


    async def enter_state(self, state):
        """Set the state of the user.

        Args:
            state: The state to set.
        """
        self.state = state
        supabase.table("session").upsert(
            {
                "id": state.session,
                "type": state.__class__.__name__,
                "user_id": self.user_id,
            }
        ).execute()
        supabase.table("users").update({"session": state.session}).eq(
            "user_id", self.user_id
        ).execute()
        print("Entered state", state.__class__.__name__, state.session)
        await state.start()
        # save context
        supabase.table("session").update({"context": state.context}).eq(
            "id", state.session
        ).execute()


async def test_new_user():
    """Test the bot with a new user."""
    user = User("test_user4")
    # assert user.state.__class__.__name__ == "WelcomeUser"
    print(user.state.__class__.__name__)
    assert user.language == "es"
    assert user.state.messages == []
    start_msg = await user.state.start()
    print(start_msg)


if __name__ == "__main__":
    # Test the bot
    import asyncio

    asyncio.run(test_new_user())
