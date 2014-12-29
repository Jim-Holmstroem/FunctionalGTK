def component(Component):
    """
    {
        label = gtk.Label('label')
        label.set_size_request(640, 480)
        label.set_justify(gtk.JUSTIFY_FILL)
    } =>
    {
        Label = component(gtk.Label)
        label = Label(
            'label',
            size_request=(640, 480),
            justify=gtk.JUSTIFY_FILL
        )
    }
    """
    def new_style_component(*args, **kwargs):
        component = Component(*args)

        def set_property(name, values):
            getattr(
                component,
                "set_{name}".format(name=name)
            )(
                *(values if isinstance(values, Iterable) else (values, ))
            )

        map(
            partial(apply, set_property),
            kwargs.iteritems()
        )

        return component

    return new_style_component


def attributes(**kwargs):
    """
    Label(
        'text',
        attributes=attributes(
            Scale=3,
            Stretch=pango.STRETCH_EXPANDED
        )
    )

    Note
    ----
    At it's current state it always force the attributes on the entire
    component.
    See. start_index, end_index
    """
    pango = __import__('pango')
    attr_list = pango.AttrList()

    def attribute(name, values):
        return getattr(
            pango,
            "Attr{name}".format(name=name)
        )(
            *(values if isinstance(values, Iterable) else (values, )),
            **{'start_index': 0, 'end_index': -1}
        )

    attributes = map(
        partial(apply, attribute),
        kwargs.iteritems()
    )
    map(
        attr_list.insert,
        attributes
    )

    return attr_list
