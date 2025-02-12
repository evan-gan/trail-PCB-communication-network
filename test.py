# from machine import Pin
# from utime import sleep

# pin = Pin("LED", Pin.OUT)

# print("LED starts flashing...")
# while True:
#     try:
#         pin.toggle()
#         sleep(1) # sleep 1sec
#     except KeyboardInterrupt:
#         break
# pin.off()
# print("Finished.")















# import machine

# # Get the unique ID
# unique_id = machine.unique_id()

# # Print the unique ID
# print("Unique ID:", unique_id)







# #Datastore test
# import ujson

# # Define your array
# array_to_store = {
#     'displayName': '', #type: ignore
#     'MSG_Draft': '', # type: ignore
#     'history': ["Please type your name and press enter"] # type: ignore
# }

# # Function to write array to flash memory
# def write_array_to_flash(filename, array):
#     try:
#         # Serialize array to JSON string
#         json_str = ujson.dumps(array)
        
#         # Write JSON string to a file
#         with open(filename, 'w') as file:
#             file.write(json_str)
#         print("Array written to flash memory successfully.")
#     except Exception as e:
#         print(f"Error writing to flash memory: {e}")

# # Function to read array from flash memory
# def read_array_from_flash(filename):
#     try:
#         # Read JSON string from the file
#         with open(filename, 'r') as file:
#             json_str = file.read()
        
#         # Deserialize JSON string to array
#         array = ujson.loads(json_str)
#         print("Array read from flash memory successfully.")
#         return array
#     except Exception as e:
#         print(f"Error reading from flash memory: {e}")
#         return None

# # Example usage
# filename = "history_data.json"

# # Write array to flash memory
# # write_array_to_flash(filename, array_to_store)

# # Read array from flash memory
# retrieved_array = read_array_from_flash(filename)

# print("Retrieved Array:", retrieved_array, "\nHistory value:", retrieved_array["history"])
