from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from core.models import Document

# Vista de login
def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('document_list')
        else:
            return HttpResponse("Invalid credentials")

    return render(request, 'frontend/login.html')

# Vista de logout
def logout_view(request):
    logout(request)
    return redirect('login')

# Vista de registro
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'frontend/register.html', {'form': form})

# Vista para ver documentos
@login_required
def document_list(request):
    # Obtener los documentos accesibles para el usuario según sus grupos
    user_groups = request.user.groups.all()
    accessible_documents = Document.objects.filter(groups__in=user_groups).distinct()

    # Verificar los permisos del usuario
    can_add = request.user.has_perm('core.add_document')
    can_change = request.user.has_perm('core.change_document')
    can_delete = request.user.has_perm('core.delete_document')

    return render(request, 'frontend/document_list.html', {
        'documents': accessible_documents,
        'can_add': can_add,
        'can_change': can_change,
        'can_delete': can_delete
    })

@login_required
@permission_required('core.add_document', raise_exception=True)
def add_document(request):
    if request.method == 'POST':
        title = request.POST['title']
        path = request.POST['path']
        mime_type = request.POST['mime_type']
        size_bytes = request.POST['size_bytes']
        document = Document(
            title=title,
            path=path,
            mime_type=mime_type,
            size_bytes=size_bytes,
            local_create_time=request.POST.get('local_create_time', None),
            server_create_time=request.POST.get('server_create_time', None),
            owner=request.user
        )
        document.save()
        return redirect('document_list')

    return render(request, 'frontend/add_document.html')

# Vista para editar un documento
@login_required
@permission_required('core.change_document', raise_exception=True)
def edit_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)

    if request.method == 'POST':
        document.title = request.POST['title']
        document.path = request.POST['path']
        document.save()
        return redirect('document_list')

    return render(request, 'frontend/edit_document.html', {'document': document})

# Vista para eliminar un documento
@login_required
@permission_required('core.delete_document', raise_exception=True)
def delete_document(request, doc_id):
    document = get_object_or_404(Document, id=doc_id)
    document.delete()
    return redirect('document_list')