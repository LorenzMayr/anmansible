class PushToAnsible(Script):
    device = ObjectVar(
        model=Device,
        description="Device to push config",
    )

    def run(self, data, commit):
        device = data["device"]

        # Get the rendered config from NetBox
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

        # POST the payload to an Ansible endpoint (e.g., your local server)
        response = requests.post("http://10.201.145.251:8080/configure", json=payload)

        # Log the response from Ansible
        self.log_info(f"Config sent to Ansible. Status: {response.status_code}")