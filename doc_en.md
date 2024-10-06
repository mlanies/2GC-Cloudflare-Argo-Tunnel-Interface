### Create a Tunnel
1. Log in to <a href="https://one.dash.cloudflare.com/" target="_blank">Zero Trust</a> and go to the Networks / Tunnels section.

2. elect "Create a tunnel."

3. Choose Cloudflared as the connector type and click Next.

4. Enter a name for your tunnel. We recommend choosing a name that reflects the type of resources you want to connect through this tunnel (e.g., SRV-01).

5. Click Save Tunnel.

6. Next, you will need to install cloudflared and run it. Make sure the environment under "Choose an operating system:" matches the operating system on your computer. Then, copy the command in the field below and paste it into the terminal of your operating system.

7. Run the command.

<div id="header"> <img src="https://developers.cloudflare.com/_astro/connector.DgDJjokf_IrBTB.webp"/> </div>
Once the command is completed, your connector will appear in Zero Trust.

8. Click Next.

9. In the "Public Hostname" tab, choose a domain and specify the subdomain or path information.

10. In the "Service Type" field, specify rdp or ssh and the URL, such as https://localhost:3389 (depending on the internal port of your service).

11. In the Additional Application Settings section, specify any parameters you would like to add to the tunnel configuration (optional).

12. Click Save Tunnel.

You can now insert the provided DNS into [2GC FREE RDP or 2GC FREE SSH](https://2gc.ru/download)  and connect to the host via Argo Tunnel.
