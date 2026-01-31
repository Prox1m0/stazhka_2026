from aiogram.fsm.state import State, StatesGroup


class OrderForm(StatesGroup):
    name = State()
    task = State()
    contact = State()


class AdminForm(StatesGroup):
    
    editing_greeting = State()

    
    adding_button_text = State()         
    adding_button_action = State()       
    adding_button_content = State()      
    adding_button_url = State()          

    deleting_button = State()            

    editing_button = State()            
    editing_button_field = State()       
    editing_button_text = State()        
    editing_button_content = State()     
    editing_button_url = State()         

