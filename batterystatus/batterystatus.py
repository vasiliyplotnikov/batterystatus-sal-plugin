from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager
from django.template import loader, Context
from django.db.models import Count, Q
from server.models import *
from django.shortcuts import get_object_or_404
import server.utils as utils

class BatteryStatus(IPlugin):
    def widget_width(self):
        return 4

    def plugin_type(self):
        return 'builtin'

    def get_description(self):
        return 'Battery status'

    def widget_content(self, page, machines=None, theid=None):
        if page == 'front':
            t = loader.get_template('plugins/traffic_lights_front.html')

        if page == 'bu_dashboard':
            t = loader.get_template('plugins/traffic_lights_front.html')

        if page == 'group_dashboard':
            t = loader.get_template('plugins/traffic_lights_id.html')

        battery_cycles_ok = machines.filter(facts__fact_name='mac_battery_cycles', facts__fact_data__lt='500').count()
        battery_cycles_warning = machines.filter(facts__fact_name='mac_battery_cycles', facts__fact_data__range=['500', '899']).count()
        battery_cycles_alert = machines.filter(
            Q(facts__fact_name='mac_battery_cycles', facts__fact_data__gte='900') |
            Q(facts__fact_name='mac_battery_health', facts__fact_data='False')).count()

        c = Context({
        'title': 'Battery Status',
        'ok_label': '< 500',
        'ok_count': battery_cycles_ok,
        'warning_label': '500 +',
        'warning_count': battery_cycles_warning,
        'alert_label': '900 +',
        'alert_count': battery_cycles_alert,
        'plugin': 'BatteryStatus',
        'theid': theid,
        'page': page
        })
        return t.render(c)

    def filter_machines(self, machines, data):
        if data == 'ok':
            machines = machines.filter(facts__fact_name='mac_battery_cycles', facts__fact_data__lt='500')
            title = 'Machines with less than 500 battery cycles'

        elif data == 'warning':
            machines = machines.filter(facts__fact_name='mac_battery_cycles', facts__fact_data__range=['500', '899'])
            title = 'Machines with 500-899 battery cycles'

        elif data == 'alert':
            machines = machines.filter(
                Q(facts__fact_name='mac_battery_cycles', facts__fact_data__gte='900') |
                Q(facts__fact_name='mac_battery_health', facts__fact_data='False'))
            title = 'Machines with more than 900 battery cycles and/or battery error'

        else:
            machines = None
        return machines, title
