from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(
            attrs={"id": "image", "class": "form-control-file btn btn-primary"}
        )
    )

    class Meta:
        model = Article
        fields = [
            "title",
            "content",
            "category",
            "image",
        ]

    def __init__(self, *args, **kwargs):
        super(ArticleForm, self).__init__(*args, **kwargs)
        self.fields["title"].widget.attrs["placeholder"] = "Enter title"
        self.fields["content"].widget.attrs["placeholder"] = "Enter content"
        self.fields["category"].widget.attrs["placeholder"] = "Select category"
        # self.fields["image"].widget.attrs["placeholder"] = "Enter image"
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control input-lg"
