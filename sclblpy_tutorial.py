import sclblpy as sp

# Make an account
print(sp.register_('your name', 'your company', 'youremail@gmail.com', 'strong_password'))
# It is recommended to also add your job title and phone number when registering


# If you already have an account, log in directly
print(sp.log_in('youremail@gmail.com', 'strong_password'))

# Register a device
print(sp.add_device('Device_test'))
# You can also provide the runtime, and the device type and serial

# In order to use your device, you'll need its uuid, you can use the get_all_devices
# function to list all devices of your organisation
devices = sp.get_all_devices()
print(devices)

# get the uuid of your device
for device in devices:
    if device['Name'] == "Your_device_name":
        device_uuid = device['UUID']
        print(device_uuid)

# Upload an onnx model
print(sp.upload_model('model_name', 'some documentation', 'input driver', 'output driver', path='your_model.onnx'))

# To see your uploaded model you can use the below function to list all models of your organisation
models = sp.get_all_models()
print(models)

# Get the uuid of your model
for model in models:
    if model['Name'] == 'Your_model_name':
        model_uuid = model['UUID']
        print(model_uuid)

# Assign a model to a device
print(sp.assign_model_to_device('device_uuid', 'model_uuid'))


# Update a model
print(sp.update_model('uuid', 'name', 'doc', 'input_driver', 'output_driver'))

# Delete a model
print(sp.delete_model(('uuid')))


