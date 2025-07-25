import pyautogui
import time
from datetime import datetime

def get_mouse_position():
    """Function to get the current mouse position"""
    while True:
        x, y = pyautogui.position()
        position_str = f"X: {x}, Y: {y}"
        print(position_str, end='\r')
        time.sleep(0.1)  # Short delay to prevent excessive CPU usage

def monitor_and_click():
    """Monitors specific coordinates and clicks when target color is detected"""
    print("Monitoring started. Press Ctrl+C to stop.")
    check_position = (1519, 1064)
    target_position = (1763, 1068)
    target_color = (253, 42, 8)
    
    # Smaller scan radius for faster processing
    scan_radius = 3
    last_click_time = 0
    cooldown = 1.0  # Reduced cooldown time
    
    while True:
        check_color = pyautogui.pixel(*check_position)
        current_time = time.time()
        
        if check_color != (0, 0, 0) and current_time - last_click_time > cooldown:
            # Optimize scan pattern - check center first, then outward
            found = False
            # Check center first
            try:
                pixel_color = pyautogui.pixel(*target_position)
                if (abs(pixel_color[0] - target_color[0]) < 10 and
                    abs(pixel_color[1] - target_color[1]) < 10 and
                    abs(pixel_color[2] - target_color[2]) < 10):
                    
                    # Immediately click when target color is found
                    pyautogui.click(target_position)
                    last_click_time = current_time
                    print(f"Clicked at {target_position} at {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
                    found = True
            except:
                pass
                
            # If not found at center, scan around
            if not found:
                for x_offset in range(-scan_radius, scan_radius + 1):
                    for y_offset in range(-scan_radius, scan_radius + 1):
                        if x_offset == 0 and y_offset == 0:
                            continue  # Skip center as we already checked it
                        
                        scan_x = target_position[0] + x_offset
                        scan_y = target_position[1] + y_offset
                        
                        try:
                            pixel_color = pyautogui.pixel(scan_x, scan_y)
                            if (abs(pixel_color[0] - target_color[0]) < 10 and
                                abs(pixel_color[1] - target_color[1]) < 10 and
                                abs(pixel_color[2] - target_color[2]) < 10):
                                
                                # Immediately click when target color is found
                                pyautogui.click(target_position)
                                last_click_time = current_time
                                print(f"Clicked at {target_position} - found at {scan_x}, {scan_y} at {datetime.now().strftime('%H:%M:%S.%f')[:-3]}")
                                found = True
                                break
                        except:
                            pass
                    if found:
                        break
                
        # Even shorter delay between checks
        time.sleep(0.001)  # 1ms delay for faster checking

# Call the function to start monitoring and clicking
if __name__ == "__main__":
    try:
        monitor_and_click()
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")