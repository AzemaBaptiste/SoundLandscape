# -*- coding: utf-8 -*-
import flask


def not_found(error, metainfo={}):
    body = {
        "success": False,
        "error": error
    }
    body.update(metainfo)

    return flask.make_response(flask.jsonify(body), 404)


def bad_request(error, metainfo={}):
    body = {
        "success": False,
        "error": error
    }
    body.update(metainfo)

    return flask.make_response(flask.jsonify(body), 400)


def created_resource(data):
    body = {
        "success": True,
        "result": data
    }

    return flask.make_response(flask.jsonify(body), 201)


def created_demand(data):
    body = {
        "success": True,
        "status": data
    }
    resp = flask.make_response(flask.jsonify(body), 202)
    resp.autocorrect_location_header = False
    resp.headers["location"] = "/jobs/{}".format(data)

    return resp


def processing(data):
    body = {
        "success": True,
        "result": data
    }

    return flask.make_response(flask.jsonify(body), 102)


def busy(data):
    body = {
        "success": False,
        "result": data
    }

    return flask.make_response(flask.jsonify(body), 409)


def get_resource(data):
    body = {
        "success": True,
        "result": data
    }

    return flask.make_response(flask.jsonify(body), 200)
