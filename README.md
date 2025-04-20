# nagios-teams-notify

Send Nagios alerts using Webhooks with Workflows for Microsoft Teams

## Overview

This script can send Nagios alerts to a Microsoft Teams channel.
This script is intended as a replacement for [the script from Isaac J. Galvan](https://github.com/isaac-galvan/nagios-teams-notify), since the old Teams notifications web hooks are no longer supported since the end of 2024.

By sending alerts to Teams, we can simplify addition and removal alert recipients, allow for self-service subscription and push preferences, and have conversations based around the alerts as they occur.

## Installation

Install dependencies

```
apk add python3 py3-pip py3-requests
```

Place `notify-teams-workflow.py` where it can be executed by the Nagios user. Make the script executable with `chmod +x notify-teams-workflow.py`.

## Configuration

### Create the Webhook

See [Create incoming webhooks with Workflows for Microsoft Teams](https://support.microsoft.com/en-us/office/create-incoming-webhooks-with-workflows-for-microsoft-teams-8ae491c7-0394-4861-ba59-055e33f75498)

### Configure Nagios

Create a command object in the Nagios configuration.

```
define command {
    command_name notify-service-by-teams
    command_line /usr/bin/python3 [path]/notify-teams-workflow.py "$_CONTACTWEBHOOKURL$" "$NOTIFICATIONTYPE$: $HOSTALIAS$/$SERVICEDESC$ is $SERVICESTATE$" "$SERVICEOUTPUT$"
}

define command {
    command_name notify-host-by-teams
    command_line /usr/bin/python3 [path]/notify-teams-workflow.py "$_CONTACTWEBHOOKURL$" "$NOTIFICATIONTYPE$: $HOSTALIAS$ is $HOSTSTATE$" "$HOSTOUTPUT$"
}
```

Create a contact object with the custom variable macro \_WEBHOOK set to the URL from the Teams channel connector. This variable is used when running the command above.

```
define contact {
    contact_name    example-team
    alias           Example Team
    host_notifications_enabled  1
    service_notifications_enabled   1
    host_notification_period	24x7
    service_notification_period	24x7
    host_notification_options	d,u,r,f,s
    service_notification_options	w,u,c,r,f
    host_notification_commands	    notify-host-by-teams
    service_notification_commands	notify-service-by-teams
    _WEBHOOKURL https://[...].logic.azure.com:443/workflows/[...]
}
```

Then add the contact to an existing object or contact group and reload your configuration.

Create additional contacts with their own `_WEBHOOKURL` custom variable macro for each Teams channel needing notifications.

## Credits

I have successfully tested this script on [the Docker image from Nagios from Christos Manios](https://github.com/manios/docker-nagios)
