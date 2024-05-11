from flask import Blueprint, render_template


dashboard_controller = Blueprint('dashboard_controller', __name__, template_folder='templates')

@dashboard_controller.route('/', methods=['GET'])
def index():
  return render_template(
    'dashboard/index.html'
  )
