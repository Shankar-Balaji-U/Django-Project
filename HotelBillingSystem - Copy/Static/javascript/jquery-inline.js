/*global DateTimeShortcuts, SelectFilter*/
/**
 * Django admin inlines
 *
 * Based on jQuery Formset 1.1
 * @author Stanislaus Madueke (stan DOT madueke AT gmail DOT com)
 * @requires jQuery 1.2.6 or later
 *
 * Copyright (c) 2009, Stanislaus Madueke
 * All rights reserved.
 *
 * Spiced up with Code from Zain Memon's GSoC project 2009
 * and modified for Django by Jannis Leidel, Travis Swicegood and Julien Phalip.
 *
 * Licensed under the New BSD License
 * See: https://opensource.org/licenses/bsd-license.php
 * file: django/contrib/admin/static/admin/js/inlines.js
 */


'use strict';
(function($) {
	$.fn.formset = function(opts) {
		const options = $.extend({}, $.fn.formset.defaults, opts);
		const $this = $(this);
		const $parent = $this.parent();
		const updateElementIndex = function(el, prefix, ndx) {
			const id_regex = new RegExp("(" + prefix + "-(\\d+|__prefix__))");
			
			const replacement = prefix + "-" + ndx;
			const table_count = ndx - 1;
			if ($(el).prop("for")) {
				$(el).prop("for", $(el).prop("for").replace(id_regex, replacement));
			}
			if (el.id) {
				el.id = el.id.replace(id_regex, replacement);
			}
			if (el.name) {
				el.name = el.name.replace(id_regex, replacement);
			}
		};
		const totalForms = $("#id_" + options.prefix + "-TOTAL_FORMS").prop("autocomplete", "off");
		let nextIndex = parseInt(totalForms.val(), 10);
		const maxForms = $("#id_" + options.prefix + "-MAX_NUM_FORMS").prop("autocomplete", "off");
		const minForms = $("#id_" + options.prefix + "-MIN_NUM_FORMS").prop("autocomplete", "off");
		let addButton;

		/**
		 * The "Add another MyModel" button below the inline forms.
		 */
		const addInlineAddButton = function() {
			/* Custom Setup for total value column */
			const tdGap = 2;
			const td = "<td></td>";
			const tdDisplayTotal = '<input type="number" tabindex="-1" name="grandtotal-'+ options.prefix + '" readonly="true" class="form-control" id="id_grandtotal-' + options.prefix + '">'
			/* endCustom Setup */
			if (addButton === null) {
				if ($this.prop("tagName") === "TR") {
					// If forms are laid out as table rows, insert the
					// "add" button in a new table row:
					const numCols = $this.eq(-1).children().length;
					if(options.firstValuePrefix && options.secondValuePrefix && options.subTotalPrefix){
						// addSubTostal(0);             // 0 -> is the index value
						// addGrandTotasl(1);           // 1 -> is the No. of the row
						$parent.after('<tfoot><tr><td colspan="' + (tdGap) + '"><button type="button" class="' + options.addCssClass + '">' + options.addText + "</button></td>" + (td.repeat(numCols - (tdGap*2))) + '<td colspan="' + tdGap + '">' + tdDisplayTotal + "</td>" + "</tr></tfoot>");
					} else {
						$parent.after('<tfoot><tr><td colspan="' + (numCols) + '"><button type="button" class="' + options.addCssClass + '">' + options.addText + "</button></td></tr></tfoot>");
					}
					
					addButton = $parent.next().find("tr:last button");
				} else {
					// Otherwise, insert it immediately after the last form:
					$this.filter(":last").after('<div><button class="' + options.addCssClass + '">' + options.addText + "</button></div>");
					addButton = $this.filter(":last").next().find("button");
				}
			}
			addButton.on('click', addInlineClickHandler);
		};

		const addInlineClickHandler = function(e) {
			const template = $("#" + options.prefix + "-empty");
			const row = template.clone(true);
			row.removeClass(options.emptyCssClass)
				.addClass(options.formCssClass)
				.attr("id", options.prefix + "-" + nextIndex);
			console.log(`Added new row: ${nextIndex+1}`);
			addInlineDeleteButton(row);
			row.find("*").each(function() {
				updateElementIndex(this, options.prefix, totalForms.val());
			});
			// Insert the new form when it has been fully edited.
			row.insertBefore($(template));
			// Update number of total forms.
			$(totalForms).val(parseInt(totalForms.val(), 10) + 1);
			nextIndex++;
			// Hide the add button if there's a limit and it's been reached.
			if ((maxForms.val() !== '') && (maxForms.val() - totalForms.val()) <= 0) {
				addButton.parent().hide();
			}
			// Show the remove buttons if there are more than min_num.
			toggleDeleteButtonVisibility(row.closest('.inline-group'));

			// Pass the new form to the post-add callback, if provided.
			if (options.added) {
				options.added(row);
			}
			$(document).trigger('formset:added', [row, options.prefix]);
			focusOnElement(nextIndex);
			updateTableIndex(totalForms.val());
			updateFormTotal(totalForms.val());
			srollToFocus(options.prefix + "-" + (nextIndex - 1));

		};
		// focusPrefix
		/**
		 * The "X" button that is part of every unsaved inline.
		 * (When saved, it is replaced with a "Delete" checkbox.)
		 */
		const addInlineDeleteButton = function(row) {
			/* 
			row.children(':last').children().is('input[type=checkbox]')
			checks wheather the DELETE column has have input tag, 
			bcos if there is an input tag then it must be already a save inlineformset */
			if (row.is("tr")) {
				if (row.children(':first').children(':last').val() == '' ) {
					// If the forms are laid out in table rows, insert
					// the remove button into the last table cell:
					row.children(":last").html('')
					row.children(":last").append('<button type="button" class="btn btn-danger btn-sm ' + options.deleteCssClass + '">' + options.deleteText + "</button>");
				}	
			} else if (row.is("ul") || row.is("ol")) {
				// If they're laid out as an ordered/unordered list,
				// insert an <li> after the last list item:
				row.append('<li><button type="button" class="btn btn-danger btn-sm ' + options.deleteCssClass + '">' + options.deleteText + "</button></li>");
			} else {
				// Otherwise, just insert the remove button as the
				// last child element of the form's container:
				row.children(":first").append('<span><button type="button" class="btn btn-danger btn-sm ' + options.deleteCssClass + '">' + options.deleteText + "</button></span>");
			}
			// Add delete handler for each row.
			row.find("button." + options.deleteCssClass).on('click', inlineDeleteHandler.bind(this));
		};

		const inlineDeleteHandler = function(e) {
			const deleteButton = $(e.target);
			const row = deleteButton.closest('.' + options.formCssClass);
			const inlineGroup = row.closest('.inline-group');
			// Remove the parent form containing this button,
			// and also remove the relevant row with non-field errors:
			const prevRow = row.prev();
			if(nextIndex > 1) {
				if (prevRow.length && prevRow.hasClass('row-form-errors')) {
					prevRow.remove();
				}
				row.remove();
				nextIndex -= 1;
				console.log(`${prevRow.index()+2} row was deleted`);
				// Pass the deleted form to the post-delete callback, if provided.
				if (options.removed) {
					options.removed(row);
				}

				$(document).trigger('formset:removed', [row, options.prefix]);
				// Update the TOTAL_FORMS form count.
				const forms = $("." + options.formCssClass);
				$("#id_" + options.prefix + "-TOTAL_FORMS").val(forms.length);
				// Show add button again once below maximum number.
				if ((maxForms.val() === '') || (maxForms.val() - forms.length) > 0) {
					addButton.parent().show();
				}
				// Hide the remove buttons if at min_num.
				toggleDeleteButtonVisibility(inlineGroup);
				// Also, update names and ids for all remaining form controls so
				// they remain in sequence:
				let i, formCount;
				const updateElementCallback = function() {
					updateElementIndex(this, options.prefix, i);
				};
				for (i = 0, formCount = forms.length; i < formCount; i++) {
					updateElementIndex($(forms).get(i), options.prefix, i);
					$(forms.get(i)).find("*").each(updateElementCallback);
				}
				updateFormTotal(totalForms.val());
				// focusOnElement(nextIndex-1);      // the get the previous index (nextIndex-1)
				updateTableIndex(totalForms.val());
			} else {
				console.log("Can't delete because a row is required.");
			}
		};

		const toggleDeleteButtonVisibility = function(inlineGroup) {
			if ((minForms.val() !== '') && (minForms.val() - totalForms.val()) >= 0) {
				inlineGroup.find('.' + options.deleteCssClass).hide();
			} else {
				inlineGroup.find('.' + options.deleteCssClass).show();
			}
		};

		const addSubTotal = function(index) {
			var firstTotalId = `#id_${options.prefix}-${index}-${options.firstValuePrefix}`;
			var secondTotalId = `#id_${options.prefix}-${index}-${options.secondValuePrefix}`;
			var subTotalId = `#id_${options.prefix}-${index}-${options.subTotalPrefix}`;
			if(!$(subTotalId).val()) {
				$(subTotalId).val((0).toFixed(2)); // initial value
			}
			$(firstTotalId + "," + secondTotalId).on("input change", function(){
				var total = Number($(firstTotalId).val()) * Number($(secondTotalId).val());
				$(subTotalId).val(total.toFixed(2));
				addGrandTotal(nextIndex);
			});
		};

		const addGrandTotal = function(length) {
			console.log(length)
			const grandTotalId = "#id_grandtotal-" + options.prefix;
			var total=0;
			for(var index=0; index < length; index++) {
				var subTotalId = `#id_${options.prefix}-${index}-${options.subTotalPrefix}`;
				total = total + Number($(subTotalId).val());
			}
			$(grandTotalId).val(total.toFixed(2));

		};

		const focusOnElement = function(index) {
			var focusElement = `#id_${options.prefix}-${index-1}-${options.focusPrefix}`;
			$(focusElement).focus();
		};

		const updateFormTotal = function(tableIndex) {
			if(options.firstValuePrefix && options.secondValuePrefix && options.subTotalPrefix){
				for(var i=0; tableIndex > i; i++) {
					addSubTotal(i);
				}
				addGrandTotal(tableIndex);
			}
		};

		function srollToFocus(id) {
			const DISTANCE = 400;
			let element = document.getElementById(id);
			let element_distance = element.offsetTop + element.getBoundingClientRect().top;
			let tag_distance;
			if(element_distance > DISTANCE){
				tag_distance = element_distance - DISTANCE;
			} else {
				tag_distance = DISTANCE - element_distance;
			}
				document.documentElement.scrollTop = tag_distance;
			}

		const updateTableIndex = function(index) {
			var tableIndex = index - 1;
			const table_regex = new RegExp("(\\d+|__prefix__)");

			// Same as above, but spread in multiple lines

			const element = $(".form-row.dynamic-" + options.prefix + "#" +options.prefix + "-" + tableIndex + " .index");
			for(var i=0; index > i; i++) {
				const element = $(".form-row.dynamic-" + options.prefix + "#" +options.prefix + "-" + i + " .index");
				element.text(i + 1);
			}
		}

		$this.each(function(i) {
			$(this).not("." + options.emptyCssClass).addClass(options.formCssClass);
		});

		// Create the delete buttons for all unsaved inlines:
		$this.filter('.' + options.formCssClass + ':not(.has_original):not(.' + options.emptyCssClass + ')').each(function() {
			addInlineDeleteButton($(this));
		});
		toggleDeleteButtonVisibility($this);

		// Create the add button, initially hidden.
		addButton = options.addButton;
		addInlineAddButton();
		$(document).ready(function() {
			updateTableIndex(totalForms.val());
			updateFormTotal(totalForms.val());
		});
		

		// Show the add button if allowed to add more items.
		// Note that max_num = None translates to a blank string.
		const showAddButton = maxForms.val() === '' || (maxForms.val() - totalForms.val()) > 0;
		if ($this.length && showAddButton) {
			addButton.parent().show();
		} else {
			addButton.parent().hide();
		}

		return this;
	};


	/* Setup plugin defaults */
	$.fn.formset.defaults = {
		prefix: "form", // The form prefix for your django formset
		addText: "add another", // Text for the add link
		deleteText: "remove", // Text for the delete link
		addCssClass: "btn btn-primary btn-sm", // CSS class applied to the add link
		deleteCssClass: "delete-btn", // CSS class applied to the delete link
		emptyCssClass: "empty-row", // CSS class applied to the empty row
		formCssClass: "dynamic-form", // CSS class applied to each form in a formset
		focusCssClass: "focus-on", // CSS class applied to each form when add or delete on.
		added: null, // Function called each time a new form is added
		removed: null, // Function called each time a form is deleted
		addButton: null, // Existing add button to use
		firstValuePrefix: null,
		secondValuePrefix: null,
		subTotalPrefix: null,
	};


	// Tabular inlines ---------------------------------------------------------
	$.fn.tabularFormset = function(selector, options) {
		const $rows = $(this);

		const reinitDateTimeShortCuts = function() {
			// Reinitialize the calendar and clock widgets by force
			if (typeof DateTimeShortcuts !== "undefined") {
				$(".datetimeshortcuts").remove();
				DateTimeShortcuts.init();
			}
		};

		const updateSelectFilter = function() {
			// If any SelectFilter widgets are a part of the new form,
			// instantiate a new SelectFilter instance for it.
			if (typeof SelectFilter !== 'undefined') {
				$('.selectfilter').each(function(index, value) {
					const namearr = value.name.split('-');
					SelectFilter.init(value.id, namearr[namearr.length - 1], false);
				});
				$('.selectfilterstacked').each(function(index, value) {
					const namearr = value.name.split('-');
					SelectFilter.init(value.id, namearr[namearr.length - 1], true);
				});
			}
		};

		const initPrepopulatedFields = function(row) {
			row.find('.prepopulated_field').each(function() {
				const field = $(this),
					input = field.find('input, select, textarea'),
					dependency_list = input.data('dependency_list') || [],
					dependencies = [];
				$.each(dependency_list, function(i, field_name) {
					dependencies.push('#' + row.find('.field-' + field_name).find('input, select, textarea').attr('id'));
				});
				if (dependencies.length) {
					input.prepopulate(dependencies, input.attr('maxlength'));
				}
			});
		};


		$rows.formset({
			prefix: options.prefix,
			addText: options.addText,
			formCssClass: "dynamic-" + options.prefix,
			deleteCssClass: "inline-deletelink",
			deleteText: options.deleteText,
			emptyCssClass: options.emptyCssClass,
			firstValuePrefix: options.firstValuePrefix,
			secondValuePrefix: options.secondValuePrefix,
			subTotalPrefix: options.subTotalPrefix,
			focusPrefix: options.focusPrefix,
			added: function(row) {
				initPrepopulatedFields(row);
				reinitDateTimeShortCuts();
				updateSelectFilter();
			},
			addButton: options.addButton
		});
		return $rows;
	};


	$(document).ready(function() {
		$(".inline-formset").each(function() {
			const data = $(this).data(), inlineOptions = data.inlineFormset;
			let selector;
			switch(data.inlineType) {
			case "tabular":
				selector = inlineOptions.name + "-group .tabular.inline-related tbody:first > tr.form-row";
				$(selector).tabularFormset(selector, inlineOptions.options);
				break;
			}
		});
	});
})($);








