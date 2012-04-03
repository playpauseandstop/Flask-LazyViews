from flask import render_template, request


def advanced():
    return render_template('test/advanced.html', values=request.values)


def test():
    return render_template('test/test.html')
