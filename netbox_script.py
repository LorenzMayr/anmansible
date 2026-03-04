class PushToAnsible(Script):
    device = ObjectVar(
        model=Device,
        description="Device to push config",
    )

    def run(self, data, commit):
        device = data["device"]

        # Get the rendered config from NetBox
        context_data = device.get_config_context()
        context_data.update({'device': device})
        config_template = device.get_config_template()
        rendered_config = config_template.render(context_data)

        # Prepare the payload
        payload = {
            "hostname": device.name,
            "rendered_config": rendered_config
        }

        # POST the payload to the Ansible endpoint
        response = requests.post("http://10.10.10.10:8080/configure", json=payload) # Replace the IP with your Ansible IP-Address
                                                                                    # Port and Endpoint stay the same

        # Log the response from Ansible
        self.log_info(f"Config sent to Ansible. Status: {response.status_code}")
