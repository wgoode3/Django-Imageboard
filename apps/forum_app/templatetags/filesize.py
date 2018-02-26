from django import template

register = template.Library()

def filesize(value):
    try:
        if value < 1000:
            return "{}B".format(value)
        elif value < 1000000:
            val = str(float(value) / (1024))
            return "{}KB".format(val) if len(val) < 5 else "{}KB".format(val[:5])
        else:
            val = str(float(value) / (1024*1024))
            return "{}MB".format(val) if len(val) < 4 else "{}MB".format(val[:4])
    except ValueError:
        return None

register.filter('filesize', filesize)