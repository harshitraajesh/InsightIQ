# flashcard_generator.py

import google.generativeai as genai
import getpass  # For securely entering the API key
import json     # To parse the AI's response
import textwrap # For formatting the text neatly
import time     # To add a small pause

# --- 1. Import text from the other file ---
try:
    from summarizer import summary
except ImportError:
    print("Error: Could not find 'input_text.py'.")
    print("Please create it in the same directory and add a 'source_text' variable.")
    exit()

def get_user_settings():
    """Gets the API key and number of flashcards from the user."""
    
    print("--- 🤖 AI Flashcard Generator Setup ---")
    
    # Get API Key securely
    api_key = getpass.getpass("Please enter your Google AI Studio API key: ")
    
    # Get number of flashcards
    while True:
        try:
            num_cards = int(input("Enter the number of flashcards to generate: "))
            if num_cards > 0:
                break
            else:
                print("Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")
            
    return api_key, num_cards

def generate_flashcards(api_key, text, num_cards):
    """Generates the flashcards using the Google Gemini AI."""
    
    try:
        # Configure the generative AI client
        genai.configure(api_key=api_key)
        
        # Use the model we confirmed is working
        model = genai.GenerativeModel('gemini-2.5-pro') 

        # --- 2. Create the AI Prompt ---
        # We ask the AI to return a specific JSON format
        prompt = f"""
        Based on the following text, create a set of flashcards.
        
        **Constraints:**
        1.  Number of flashcards: {num_cards}
        2.  The "front" of the card should be a key term, concept, or a short question.
        3.  The "back" of the card should be the concise definition, answer, or explanation.
        
        **Output Format:**
        Provide the output as a valid JSON list. Each item in the list should
        be an object with two keys: "front" and "back".
        
        **Example JSON format:**
        [
          {{
            "front": "What is Photosynthesis?",
            "back": "The process by which green plants use sunlight to synthesize foods."
          }},
          {{
            "front": "Chemical equation for photosynthesis",
            "back": "6CO2 + 6H2O + Light Energy → C6H12O6 + 6O2"
          }}
        ]
        
        ---
        **Source Text:**
        {text}
        ---
        
        Now, generate the JSON for the {num_cards} flashcards:
        """
        
        print(f"\n🤖 Generating {num_cards} flashcards... (This may take a moment)")
        
        # --- 3. Call the API ---
        response = model.generate_content(prompt)
        
        # Clean the response to get just the JSON
        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        
        # --- 4. Parse the JSON ---
        flashcard_data = json.loads(cleaned_response)
        return flashcard_data
        
    except Exception as e:
        print(f"\n❌ An error occurred during API call or JSON parsing:")
        print(f"Error: {e}")
        print("\n--- Raw AI Response ---")
        try:
            # Try to print the raw response if it exists
            print(response.text)
        except NameError:
            print("Could not get a response from the AI. Check your API key and internet connection.")
        return None

def run_flashcard_session(flashcard_data):
    """Runs the flashcard session for the user."""
    
    print("\n--- 📇 Flashcard Session Started! ---")
    print("Press 'Enter' to flip the card. Type 'q' and 'Enter' to quit.")
    
    for i, card in enumerate(flashcard_data):
        print(f"\n--- Card {i + 1} of {len(flashcard_data)} ---")
        
        # --- 5. Display the Front ---
        front_text = textwrap.fill(f"FRONT: {card['front']}", width=80)
        print(front_text)
        
        # --- 6. Wait for user to flip ---
        user_input = input("\n...Press Enter to flip...")
        
        if user_input.lower().strip() == 'q':
            print("Quitting session.")
            break
            
        # --- 7. Display the Back ---
        back_text = textwrap.fill(f"BACK:  {card['back']}", width=80)
        print(back_text)
        
        print("-" * 80)
        time.sleep(1) # Add a small pause so the user can read
            
    print("\n--- 🎉 Session Complete! ---")
    print(f"You reviewed all {len(flashcard_data)} cards.")

# --- Main execution ---
if __name__ == "__main__":
    api_key, num_cards = get_user_settings()
    
    if api_key:
        card_content = generate_flashcards(api_key, summary, num_cards)
        
        if card_content:
            run_flashcard_session(card_content)