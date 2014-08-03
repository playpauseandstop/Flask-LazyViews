from flask import abort, render_template, request


def advanced():
    return render_template('testblueprint/advanced.html',
                           values=request.values)


def custom_error(code):
    raise abort(code)


def error(err):
    code = err.code if hasattr(err, 'code') else 500
    return (render_template('testblueprint/error.html', code=code, error=err),
            code)


def test():
    return render_template('testblueprint/test.html')
