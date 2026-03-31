
class ASService:
    def __init__(self):
        self.is_alarm_ringing = False
        self.next_alarm_time = "N/A"
        self.next_alarm_armed = False
        
        self.screen_state = True
        
        
    def set_alarm_ringing(self, ringing: bool):
        self.is_alarm_ringing = ringing
        
    def get_alarm_ringing(self) -> bool:
        return self.is_alarm_ringing
    
    def set_screen_state(self, state: bool):
        self.screen_state = state
        
    def get_screen_state(self) -> bool:
        return self.screen_state
    
    def toggle_screen_state(self):
        self.screen_state = not self.screen_state
        
    def set_alarm_time(self, alarm_time: str):
        self.next_alarm_time = alarm_time
        
    def get_alarm_time(self) -> str:
        return self.next_alarm_time
    
    def set_alarm_armed(self, armed: bool):
        self.next_alarm_armed = armed
        
    def get_alarm_armed(self) -> bool:
        return self.next_alarm_armed