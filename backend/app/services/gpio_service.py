from __future__ import annotations 
import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING, Dict, Union



from app.services.application_state_service import ASService
from app.services.alarm_service import AlarmService
from app.services.screen_service import ScreenService
    
# The driver implements these methods this class tells the service to expect them
class ButtonDriverInterface:
    def press(self) -> bool:
        """Synchronous check of the physical pin state."""
        ... # Implementation is in the HAL file
        
    def switch(self) -> bool:
        """Synchronous check of the physical pin state."""
        ... # Implementation is in the HAL file
        
    def cleanup(self):
        """Releases hardware resources."""
        ...

DriverMap = Dict[str, ButtonDriverInterface]


class GpioService:
    def __init__(
        self, 
        app_state: ASService, 
        alarm_handler: AlarmService,
        screen_handler: ScreenService,
        button_drivers: DriverMap # The driver instance is INJECTED
    ):
        self.app_state = app_state
        self.alarm_handler = alarm_handler
        self.screen_handler = screen_handler
        self.buttons: DriverMap = button_drivers
        self._polling_task: Union[asyncio.Task, None] = None

        
        # Use a dedicated thread pool for non-blocking execution of sync HAL calls
        self._executor = ThreadPoolExecutor(max_workers=5)

    def start_polling(self):
        """Creates and runs the asynchronous polling task."""
        if self._polling_task is None:
            self._polling_task = asyncio.create_task(self._poll_input_loop())
            print("GpioService: Background polling loop started.")

    async def shutdown(self):
        """Gracefully stops the polling loop and cleans up hardware."""
        if self._polling_task:
            self._polling_task.cancel()
            await asyncio.gather(self._polling_task, return_exceptions=True)
            print("GpioService: Polling loop stopped.")
        
        # Cleanup ALL button drivers
        for name, driver in self.buttons.items():
            # Hardware cleanup must also run in a thread to be non-blocking
            # We assume 'cleanup' is synchronous (like RPi.GPIO.cleanup)
            await asyncio.to_thread(driver.cleanup)
            print(f"GpioService: Cleaned up driver: {name}")

    async def _poll_input_loop(self, poll_interval=0.05):
        """
        The continuous loop that safely checks synchronous hardware state for ALL buttons.
        """
        try:
            while True:
                # Iterate over all registered buttons
                for button_name, driver_instance in self.buttons.items():
                    
                    # CRITICAL: Run the synchronous driver method in a separate thread
                    # Using the 'press' method as defined in your interface
                    # This ensures the main event loop remains responsive.
                    print("Awaiting Button Press")
                    is_pressed = await asyncio.to_thread(driver_instance.press)
                    
                    if is_pressed:
                        # Pass the unique name to the handler for dispatching
                        self._handle_button_press(button_name) 
                
                await asyncio.sleep(poll_interval)
                
        except asyncio.CancelledError:
            # Expected during graceful shutdown
            pass
        except Exception as e:
            print(f"GpioService Error in polling loop: {e}")

    def _handle_button_press(self, button_name: str):
        """Decides the action based on the unique button name and application state (SOT)."""
        
        print(f"Detected press from button: {button_name}")

        # Use match/case for clean action dispatching (requires Python 3.10+)
        # This routes the physical event to the correct business logic.
        match button_name:
            case 'Primary':
                print("Primary Button Pressed")
                if self.app_state.get_alarm_ringing() is True:
                    print("Turning off alarm")
                    self.alarm_handler.alarm_stop()
                else: 
                    self.screen_handler.toggle_display()
                    self.app_state.toggle_screen_state()

                
            
            case 'Secondary':
                print("Secondary Button Pressed")
            
            case 'Encoder':
                print("Encoder Button Pressed")

            case _:
                print(f"Warning: Unhandled button press for name: {button_name}")
               