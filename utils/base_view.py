from rest_framework import generics, mixins


class DynamicModelSerializerMixin:
    def __init__(self, model=None, serializer_class=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.model = model
        self.serializer_class = serializer_class


class BaseAPIView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    DynamicModelSerializerMixin,
    generics.GenericAPIView,
):
    def __init__(self, *args, **kwargs):
        model = kwargs.pop('model', None)
        serializer_class = kwargs.pop('serializer_class', None)
        super().__init__(
            model=model, serializer_class=serializer_class, *args, **kwargs
        )

    def get_queryset(self):
        return self.model.objects.all()

    def get_serializer_class(self):
        return self.serializer_class

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
