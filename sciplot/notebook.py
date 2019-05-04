import ipywidgets as widgets
from IPython.display import display, HTML
from IPython.display import display
from IPython.display import HTML
import IPython.core.display as di
import random


def hidecode(showbutton=False):
    if(showbutton == True):
        javascript_functions = {False: "hide()", True: "show()"}
        button_descriptions = {False: "Show code", True: "Hide code"}

        def toggle_code(state):
            output_string = "<script>$(\"div.input\").{}</script>"
            output_args = (javascript_functions[state],)
            output = output_string.format(*output_args)
            display(HTML(output))

        def button_action(value):
            state = value.new
            toggle_code(state)
            value.owner.description = button_descriptions[state]
        state = False
        toggle_code(state)
        button = widgets.ToggleButton(
            state, description=button_descriptions[state])
        button.observe(button_action, "value")
        display(button)
    else:
        di.display_html(
            '<script>jQuery(function() {if (jQuery("body.notebook_app").length == 0) { jQuery(".input_area").toggle(); jQuery(".prompt").toggle();}});</script>', raw=True)
        CSS = """#notebook div.output_subarea {max-width:100%;}"""  # changes output_subarea width to 100% (from 100% - 14ex)
        HTML('<style>{}</style>'.format(CSS))


def hidecell(for_next=False):
    this_cell = """$('div.cell.code_cell.rendered.selected')"""
    next_cell = this_cell + '.next()'
    toggle_text = '显示/隐藏'  # text shown on toggle link
    target_cell = this_cell  # target cell to control with toggle
    # bit of JS to permanently hide code in current cell (only when toggling next cell)
    js_hide_current = ''
    if for_next:
        target_cell = next_cell
        toggle_text += ' next cell'
        js_hide_current = this_cell + '.find("div.input").hide();'
    js_f_name = 'code_toggle_{}'.format(str(random.randint(1, 2**64)))
    html = """
        <script>
            function {f_name}() {{
                {cell_selector}.find('div.input').toggle();
            }}

            {js_hide_current}
        </script>
        <a href="javascript:{f_name}()">{toggle_text}</a>
    """.format(
        f_name=js_f_name,
        cell_selector=target_cell,
        js_hide_current=js_hide_current,
        toggle_text=toggle_text
    )
    return HTML(html)
