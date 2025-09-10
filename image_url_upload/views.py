from django.shortcuts import render
from wagtail.images.forms import AddImageFromURLForm
from wagtail.images import get_image_model
from wagtail.admin import messages
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

def add_url(request):
    if request.method == 'POST':
        form = AddImageFromURLForm(request.POST)
        if form.is_valid():
            try:
                # Assuming you have a function to create an image from a URL
                image_model = get_image_model()
                image = image_model.objects.create(
                    title=form.cleaned_data['image_url'],
                    file=form.cleaned_data['image_url']
                )
                messages.success(request, _('Image "%s" added.') % image.title, buttons=[
                    messages.button(
                        reverse('wagtailimages:edit', args=(image.id,)),
                        _('Edit')
                    )
                ])
                # You'll likely need to redirect to the image index or a similar page
            except Exception as e:
                messages.error(request, _("Failed to add image from URL: %s") % str(e))
    else:
        form = AddImageFromURLForm()
    
    breadcrumbs_items = [
        {'url': reverse('wagtailadmin_home'), 'label': _('Home')},
        {'url': reverse('wagtailimages:index'), 'label': _('Images')},
        {'url': reverse('wagtailimages:add_url'), 'label': _('Add image from URL')},
    ]
    
    return render(request, 'wagtailimages/add_via_url.html', {
        'form': form,
        'breadcrumbs_items': breadcrumbs_items,
    })
