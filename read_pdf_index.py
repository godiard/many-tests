from gi.repository import Gtk
from gi.repository import EvinceDocument
from gi.repository import EvinceView

EvinceDocument.init()

doc =  EvinceDocument.Document.factory_get_document('file:///home/gonzalo/Desktop/Libros/La_gran_manzana.pdf')

def job_finished_cb(job):
    model = job.get_model()
    _iter = model.get_iter_first()
    while True:
        value = model.get_value(_iter, 0)
        print value, model.get_value(_iter, 1)
        _iter = model.iter_next(_iter)
        if _iter is None:
            break

view = EvinceView.View()

model = EvinceView.DocumentModel()
model.set_document(doc)
view.set_model(model)

if not doc.has_document_links():
    print 'The pdf file does not have a index'
else:
    jl = EvinceView.JobLinks.new(document=doc)
    jl.connect('finished', job_finished_cb)
    EvinceView.Job.scheduler_push_job(jl, EvinceView.JobPriority.PRIORITY_NONE)

win = Gtk.Window()
scrolled = Gtk.ScrolledWindow()
win.add(scrolled)
scrolled.add_with_viewport(view)

win.set_default_geometry(200, 300)
win.connect("destroy", Gtk.main_quit)

win.show_all()
Gtk.main()

