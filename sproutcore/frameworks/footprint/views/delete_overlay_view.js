/**
 * Created by calthorpe on 11/18/13.
 */

Footprint.DeleteOverlayView = SC.View.extend({
    childViews: ['informOverlayView', 'errorOverlayView'],
    classNames: ['delete-overlay-view'],

    /***
     * The content whose status is being observed.
     */
    content:null,
    /***
     * The content status
     */
    status:null,
    statusBinding:SC.Binding.oneWay('*content.status'),
    isVisibleBinding: SC.Binding.oneWay('*content.deleted').bool(),
    /**
     * content key to its name
     */
    contentNameKey: null,

    informOverlayView: SC.View.extend({
        childViews:['labelView', 'imageView', 'deleteButtonView', 'cancelButtonView'],
        classNames: ['delete-inform-overlay-view'],
        isVisible:NO,
        isVisibleBinding: SC.Binding.oneWay('.parentView.status').matchesStatus(SC.Record.ERROR).not(),
        content:null,
        contentBinding:SC.Binding.oneWay('.parentView.content'),
        labelView: SC.LabelView.extend({
            layout: { centerX:0, top: 100, width:16, height:16},
            content: SC.Binding.oneWay('parentView.content'),
            contentValueKey: SC.Binding.oneWay('parentView.contentNameKey')
        }),
        imageView: SC.ImageView.extend({
            layout: { centerX:0, top: 200, width:16, height:16},
            useCanvas: NO,
            value: sc_static('footprint:images/delete.png')
        }),
        deleteButtonView: SC.ButtonView.extend({
            layout: { centerX:-100, top: 300, width:100, height:24},
            title: 'Delete',
            content: null,
            contentBinding: SC.Binding.oneWay('.parentView.content'),
            // saving with deleted=YES
            action: 'doSave'
        }),
        cancelButtonView: SC.ButtonView.extend({
            layout: { centerX:100, top: 300, width:100, height:24},
            title: 'Delete',
            content: null,
            contentBinding: SC.Binding.oneWay('.parentView.content'),
            action: 'doCancelDeleteRecord'
        })

    }),

    errorOverlayView: SC.View.extend({
        childViews:['labelView'],
        classNames: ['delete-error-overlay-view'],
        isVisible:NO,
        isVisibleBinding: SC.Binding.oneWay('.parentView.status').matchesStatus(SC.Record.ERROR),
        labelView: SC.LabelView.extend({
            layout: { centerX:0, centerY:0, width:100, height:20},
            value: 'An Error Occurred...'
        })
    })
});
