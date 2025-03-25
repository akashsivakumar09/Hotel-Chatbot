import streamlit as st
from langchain.memory import ConversationBufferWindowMemory
from langchain.tools import tool
from langchain.agents import initialize_agent, Tool
from langchain_groq import ChatGroq
from reservation import HotelReservation

# Initialize hotel reservation system
hotel_reservation = HotelReservation()

# Define tools for the agent
@tool
def book_room():
    """Book a room for the user."""
    reservation = hotel_reservation.get_reservation()
    return f"Just say the {reservation['roomtype']} room is booked to user."

@tool
def check_availability(user_details):
    """Check room availability."""
    return "Room is available on [15/06, 16/06, 17/06] dates only."

@tool
def cancel_booking():
    """Cancel a booking."""
    return "Booking cancelled successfully."

@tool
def num_rooms():
    """Giving information about the number of rooms available."""
    return "There are {'Luxury':3, 'Deluxe':5} rooms available."

@tool
def get_entity():
    """Get the Entities."""
    return "Extracting check-in date, check-out date, room type, and number of guests."

# Set up the model and tools
llm = ChatGroq(model="qwen-qwq-32b", api_key="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")

tools = [
    Tool(name="Book Room", func=book_room, description="User wants to book a room."),
    Tool(name="Check Availability", func=check_availability, description="Check room availability."),
    Tool(name="Cancel Booking", func=cancel_booking, description="Cancel a booking."),
    Tool(name="Number of room", func=num_rooms, description="Number of rooms inquiry."),
]

# Set up memory for the agent
memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)

# Initialize the agent with memory
agent = initialize_agent(
    system_message="You are a reliable hotel reservation chatbot. Select the appropriate tool based on context and respond accordingly.",
    tools=tools,
    llm=llm,
    agent="chat-conversational-react-description", 
    memory=memory, 
    verbose=True  
)

# Streamlit UI
st.title("🏨 Hotel Reservation Chatbot")

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# User input
user_input = st.chat_input("Ask about booking, availability, or cancellations...")

if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get agent response
    response = agent.invoke({"input": user_input})["output"]

    # Display chatbot response
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.write(response)
