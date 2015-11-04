# -*- coding: utf-8 -*-
from django.template import Template, Context
from django.test import TestCase


class GitHubLoginButtonTestCase(TestCase):
    context = Context({})

    def test_default_values_renders_properly(self):
        template = Template(
            """{% load github %}{% github_login %}"""
        )

        rendered = template.render(self.context)
        self.assertHTMLEqual(
            rendered,
            """
            <form action="/social/github/login/" method="post">
                <input type="hidden" name="next" value="" />
                <a class="" onclick="this.parentNode.submit()">
                    <i class=""></i><span>Sign in with GitHub</span>
                </a>
            </form>
            """
        )

    def test_custom_label_changes_button_text(self):
        template = Template(
            """{% load github %}{% github_login label="CUSTOM LABEL" %}"""
        )

        rendered = template.render(self.context)
        self.assertHTMLEqual(
            rendered,
            """
            <form action="/social/github/login/" method="post">
                <input type="hidden" name="next" value="" />
                <a class="" onclick="this.parentNode.submit()">
                    <i class=""></i><span>CUSTOM LABEL</span>
                </a>
            </form>
            """
        )

    def test_custom_css_class_is_added(self):
        template = Template(
            """{% load github %}{% github_login css_class="CUSTOM" %}"""
        )

        rendered = template.render(self.context)
        self.assertHTMLEqual(
            rendered,
            """
            <form action="/social/github/login/" method="post">
                <input type="hidden" name="next" value="" />
                <a class="CUSTOM" onclick="this.parentNode.submit()">
                    <i class=""></i><span>Sign in with GitHub</span>
                </a>
            </form>
            """
        )

    def test_custom_icon_class_is_added(self):
        template = Template(
            """{% load github %}{% github_login icon_class="CUSTOM" %}"""
        )

        rendered = template.render(self.context)
        self.assertHTMLEqual(
            rendered,
            """
            <form action="/social/github/login/" method="post">
                <input type="hidden" name="next" value="" />
                <a class="" onclick="this.parentNode.submit()">
                    <i class="CUSTOM"></i><span>Sign in with GitHub</span>
                </a>
            </form>
            """
        )

    def test_only_login_changes_label(self):
        template = Template(
            """{% load github %}{% github_login only_login=True %}"""
        )

        rendered = template.render(self.context)
        self.assertHTMLEqual(
            rendered,
            """
            <form action="/social/github/login/" method="post">
                <input type="hidden" name="only_login" value="" />
                <input type="hidden" name="next" value="" />
                <a class="" onclick="this.parentNode.submit()">
                    <i class=""></i><span>Log in with GitHub</span>
                </a>
            </form>
            """
        )

    def test_reconnection_renders_hidden_input(self):
        template = Template(
            """{% load github %}{% github_login reconnection=True %}"""
        )

        rendered = template.render(self.context)
        self.assertHTMLEqual(
            rendered,
            """
            <form action="/social/github/login/" method="post">
                <input type="hidden" name="reconnection" value="true" />
                <input type="hidden" name="next" value="" />
                <a class="" onclick="this.parentNode.submit()">
                    <i class=""></i><span>Sign in with GitHub</span>
                </a>
            </form>
            """
        )
