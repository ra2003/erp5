/*global window, rJS, RSVP, calculatePageTitle */
/*jslint nomen: true, indent: 2, maxerr: 3 */
(function (window, rJS, RSVP, calculatePageTitle) {
  "use strict";

  rJS(window)
    /////////////////////////////////////////////////////////////////
    // Acquired methods
    /////////////////////////////////////////////////////////////////
    .declareAcquiredMethod("updateHeader", "updateHeader")
    .declareAcquiredMethod("getUrlFor", "getUrlFor")
    .declareAcquiredMethod("redirect", "redirect")
    .declareAcquiredMethod("getUrlParameter", "getUrlParameter")
    .declareAcquiredMethod("renderEditorPanel", "renderEditorPanel")

    /////////////////////////////////////////////////////////////////
    // declared methods
    /////////////////////////////////////////////////////////////////
    .declareMethod('render', function (options) {
      var gadget = this;
      return gadget.getUrlParameter('extended_search')
        .push(function (extended_search) {
          var state_dict = {
            id: options.jio_key,
            view: options.view,
            editable: options.editable,
            erp5_document: options.erp5_document,
            form_definition: options.form_definition,
            erp5_form: options.erp5_form || {},
            extended_search: extended_search
          };
          return gadget.changeState(state_dict);
        });
    })

    .onStateChange(function () {
      var form_gadget = this;

      // render the erp5 form
      return form_gadget.getDeclaredGadget("erp5_form")
        .push(function (erp5_form) {
          var form_options = form_gadget.state.erp5_form;

          form_options.erp5_document = form_gadget.state.erp5_document;
          form_options.form_definition = form_gadget.state.form_definition;
          form_options.view = form_gadget.state.view;

          // XXX Hardcoded for listbox's hide functionality
          form_options.form_definition.hide_enabled = true;

          // XXX not generic, fix later
          if (form_gadget.state.extended_search) {
            form_options.form_definition.extended_search = form_gadget.state.extended_search;
          }

          return erp5_form.render(form_options);
        })

        // render the search field
        .push(function () {
          return form_gadget.getDeclaredGadget("erp5_searchfield");
        })
        .push(function (search_gadget) {
          var search_options = {};
          // XXX not generic, fix later
          if (form_gadget.state.extended_search) {
            search_options.extended_search = form_gadget.state.extended_search;
          }
          return search_gadget.render(search_options);
        })

        // render the header
        .push(function () {
          var new_content_action = form_gadget.state.erp5_document._links.action_object_new_content_action;

          if (new_content_action !== undefined) {
            new_content_action = form_gadget.getUrlFor({command: 'change', options: {view: new_content_action.href, editable: true}});
          } else {
            new_content_action = "";
          }

          return RSVP.all([
            new_content_action,
            form_gadget.getUrlFor({command: 'change', options: {page: "action"}}),
            form_gadget.getUrlFor({command: 'display', options: {}}),
            calculatePageTitle(form_gadget, form_gadget.state.erp5_document)
          ]);
        })
        .push(function (all_gadget) {
          return form_gadget.updateHeader({
            panel_action: true,
            jump_url: "",
            cut_url: "",
            add_url: all_gadget[0],
            actions_url: all_gadget[1],
            export_url: "",
            page_title: all_gadget[3],
            front_url: all_gadget[2],
            filter_action: true
          });
        });

    })

    .declareMethod('triggerSubmit', function () {
      var gadget = this,
        extended_search = '';
      return gadget.getDeclaredGadget("erp5_searchfield")
        .push(function (search_gadget) {
          return search_gadget.getContent();
        })
        .push(function (result) {
          // Hardcoded field name
          extended_search = result.search;
          return gadget.getDeclaredGadget("erp5_form");
        })
        .push(function (form_gadget) {
          return form_gadget.getListboxInfo();
        })
        .push(function (result) {
          return gadget.renderEditorPanel("gadget_erp5_search_editor.html", {
            extended_search: extended_search,
            begin_from: result.begin_from,
            search_column_list: result.search_column_list
          });
        });
    })

    .onEvent('submit', function () {
      var gadget = this;

      return gadget.getDeclaredGadget("erp5_searchfield")
        .push(function (search_gadget) {
          return search_gadget.getContent();
        })
        .push(function (data) {
          var options = {
            begin_from: undefined,
            // XXX Hardcoded
            field_listbox_begin_from: undefined
          };
          if (data.search) {
            options.extended_search = data.search;
          } else {
            options.extended_search = undefined;
          }

          return gadget.redirect({command: 'store_and_change', options: options});
        });

    }, false, true);

}(window, rJS, RSVP, calculatePageTitle));