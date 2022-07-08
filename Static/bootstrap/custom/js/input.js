
  /**
   * ----------------------------------------
   * Content for MDB
   * ----------------------------------------
   * **/

  /**
   * ------------------------------------------------------------------------
   * Import element, getjQuery, onDOMContentLoaded fuctions
   * ------------------------------------------------------------------------
   */

  const element = (tag) => {
    return document.createElement(tag);
  };

  /**
   * ------------------------------------------------------------------------
   * Import Data Class
   * ------------------------------------------------------------------------
   */

  const mapData = (() => {
    const storeData = {};
    let id = 1;
    return {
      set(element, key, data) {
        if (typeof element[key] === 'undefined') {
          element[key] = {
            key,
            id,
          };
          id++;
        }

        storeData[element[key].id] = data;
      },
      get(element, key) {
        if (!element || typeof element[key] === 'undefined') {
          return null;
        }

        const keyProperties = element[key];
        if (keyProperties.key === key) {
          return storeData[keyProperties.id];
        }

        return null;
      },
      delete(element, key) {
        if (typeof element[key] === 'undefined') {
          return;
        }

        const keyProperties = element[key];
        if (keyProperties.key === key) {
          delete storeData[keyProperties.id];
          delete element[key];
        }
      },
    };
  })();

  const CustomData = {
    setData(instance, key, data) {
      mapData.set(instance, key, data);
    },
    getData(instance, key) {
      return mapData.get(instance, key);
    },
    removeData(instance, key) {
      mapData.delete(instance, key);
    },
  };


  /**
   * ------------------------------------------------------------------------
   * Import EventHandler Class
   * ------------------------------------------------------------------------
   */

  const $ = getjQuery();


  /**
   * ------------------------------------------------------------------------
   * Private methods
   * ------------------------------------------------------------------------
   */

  function getUidEvent(element, uid) {
    return (uid && `${uid}::${uidEvent++}`) || element.uidEvent || uidEvent++;
  }

  function getEvent(element) {
    const uid = getUidEvent(element);

    element.uidEvent = uid;
    eventRegistry[uid] = eventRegistry[uid] || {};

    return eventRegistry[uid];
  }

  function bootstrapHandler(element, fn) {
    return function handler(event) {
      event.delegateTarget = element;

      if (handler.oneOff) {
        EventHandler.off(element, event.type, fn);
      }

      return fn.apply(element, [event]);
    };
  }

  function bootstrapDelegationHandler(element, selector, fn) {
    return function handler(event) {
      const domElements = element.querySelectorAll(selector);

      for (let { target } = event; target && target !== this; target = target.parentNode) {
        for (let i = domElements.length; i--; '') {
          if (domElements[i] === target) {
            event.delegateTarget = target;

            if (handler.oneOff) {
              EventHandler.off(element, event.type, fn);
            }

            return fn.apply(target, [event]);
          }
        }
      }

      // To please ESLint
      return null;
    };
  }

  function findHandler(events, handler, delegationSelector = null) {
    const uidEventList = Object.keys(events);

    for (let i = 0, len = uidEventList.length; i < len; i++) {
      const event = events[uidEventList[i]];

      if (event.originalHandler === handler && event.delegationSelector === delegationSelector) {
        return event;
      }
    }

    return null;
  }

  function normalizeParams(originalTypeEvent, handler, delegationFn) {
    const delegation = typeof handler === 'string';
    const originalHandler = delegation ? delegationFn : handler;

    // allow to get the native events from namespaced events ('click.bs.button' --> 'click')
    let typeEvent = originalTypeEvent.replace(stripNameRegex, '');
    const custom = customEvents[typeEvent];

    if (custom) {
      typeEvent = custom;
    }

    const isNative = nativeEvents.has(typeEvent);

    if (!isNative) {
      typeEvent = originalTypeEvent;
    }

    return [delegation, originalHandler, typeEvent];
  }

  function addHandler(element, originalTypeEvent, handler, delegationFn, oneOff) {
    if (typeof originalTypeEvent !== 'string' || !element) {
      return;
    }

    if (!handler) {
      handler = delegationFn;
      delegationFn = null;
    }

    const [delegation, originalHandler, typeEvent] = normalizeParams(
      originalTypeEvent,
      handler,
      delegationFn
    );
    const events = getEvent(element);
    const handlers = events[typeEvent] || (events[typeEvent] = {});
    const previousFn = findHandler(handlers, originalHandler, delegation ? handler : null);

    if (previousFn) {
      previousFn.oneOff = previousFn.oneOff && oneOff;

      return;
    }

    const uid = getUidEvent(originalHandler, originalTypeEvent.replace(namespaceRegex, ''));
    const fn = delegation
      ? bootstrapDelegationHandler(element, handler, delegationFn)
      : bootstrapHandler(element, handler);

    fn.delegationSelector = delegation ? handler : null;
    fn.originalHandler = originalHandler;
    fn.oneOff = oneOff;
    fn.uidEvent = uid;
    handlers[uid] = fn;

    element.addEventListener(typeEvent, fn, delegation);
  }

  function removeHandler(element, events, typeEvent, handler, delegationSelector) {
    const fn = findHandler(events[typeEvent], handler, delegationSelector);

    if (!fn) {
      return;
    }

    element.removeEventListener(typeEvent, fn, Boolean(delegationSelector));
    delete events[typeEvent][fn.uidEvent];
  }

  function removeNamespacedHandlers(element, events, typeEvent, namespace) {
    const storeElementEvent = events[typeEvent] || {};

    Object.keys(storeElementEvent).forEach((handlerKey) => {
      if (handlerKey.indexOf(namespace) > -1) {
        const event = storeElementEvent[handlerKey];

        removeHandler(element, events, typeEvent, event.originalHandler, event.delegationSelector);
      }
    });
  }

  const CustomEventHandler = {
    on(element, event, handler, delegationFn) {
      addHandler(element, event, handler, delegationFn, false);
    },

    one(element, event, handler, delegationFn) {
      addHandler(element, event, handler, delegationFn, true);
    },

    off(element, originalTypeEvent, handler, delegationFn) {
      if (typeof originalTypeEvent !== 'string' || !element) {
        return;
      }

      const [delegation, originalHandler, typeEvent] = normalizeParams(
        originalTypeEvent,
        handler,
        delegationFn
      );
      const inNamespace = typeEvent !== originalTypeEvent;
      const events = getEvent(element);
      const isNamespace = originalTypeEvent.charAt(0) === '.';

      if (typeof originalHandler !== 'undefined') {
        // Simplest case: handler is passed, remove that listener ONLY.
        if (!events || !events[typeEvent]) {
          return;
        }

        removeHandler(element, events, typeEvent, originalHandler, delegation ? handler : null);
        return;
      }

      if (isNamespace) {
        Object.keys(events).forEach((elementEvent) => {
          removeNamespacedHandlers(element, events, elementEvent, originalTypeEvent.slice(1));
        });
      }

      const storeElementEvent = events[typeEvent] || {};
      Object.keys(storeElementEvent).forEach((keyHandlers) => {
        const handlerKey = keyHandlers.replace(stripUidRegex, '');

        if (!inNamespace || originalTypeEvent.indexOf(handlerKey) > -1) {
          const event = storeElementEvent[keyHandlers];

          removeHandler(element, events, typeEvent, event.originalHandler, event.delegationSelector);
        }
      });
    },

    trigger(element, event, args) {
      if (typeof event !== 'string' || !element) {
        return null;
      }

      const typeEvent = event.replace(stripNameRegex, '');
      const inNamespace = event !== typeEvent;
      const isNative = nativeEvents.has(typeEvent);

      let jQueryEvent;
      let bubbles = true;
      let nativeDispatch = true;
      let defaultPrevented = false;
      let evt = null;

      if (inNamespace && $) {
        jQueryEvent = $.Event(event, args);

        $(element).trigger(jQueryEvent);
        bubbles = !jQueryEvent.isPropagationStopped();
        nativeDispatch = !jQueryEvent.isImmediatePropagationStopped();
        defaultPrevented = jQueryEvent.isDefaultPrevented();
      }

      if (isNative) {
        evt = document.createEvent('HTMLEvents');
        evt.initEvent(typeEvent, bubbles, true);
      } else {
        evt = new CustomEvent(event, {
          bubbles,
          cancelable: true,
        });
      }

      // merge custom informations in our event
      if (typeof args !== 'undefined') {
        Object.keys(args).forEach((key) => {
          Object.defineProperty(evt, key, {
            get() {
              return args[key];
            },
          });
        });
      }

      if (defaultPrevented) {
        evt.preventDefault();
      }

      if (nativeDispatch) {
        element.dispatchEvent(evt);
      }

      if (evt.defaultPrevented && typeof jQueryEvent !== 'undefined') {
        jQueryEvent.preventDefault();
      }

      return evt;
    },
  };

  /**
   * ------------------------------------------------------------------------
   * Import Manipulator Class
   * ------------------------------------------------------------------------
   */

  function normalizeData(val) {
    if (val === 'true') {
      return true;
    }

    if (val === 'false') {
      return false;
    }

    if (val === Number(val).toString()) {
      return Number(val);
    }

    if (val === '' || val === 'null') {
      return null;
    }

    return val;
  }

  function normalizeDataKey(key) {
    return key.replace(/[A-Z]/g, (chr) => `-${chr.toLowerCase()}`);
  }

  const CustomManipulator = {
    setDataAttribute(element, key, value) {
      element.setAttribute(`data-mdb-${normalizeDataKey(key)}`, value);
    },

    removeDataAttribute(element, key) {
      element.removeAttribute(`data-mdb-${normalizeDataKey(key)}`);
    },

    getDataAttributes(element) {
      if (!element) {
        return {};
      }

      const attributes = {
        ...element.dataset,
      };

      Object.keys(attributes)
        .filter((key) => key.startsWith('mdb'))
        .forEach((key) => {
          let pureKey = key.replace(/^mdb/, '');
          pureKey = pureKey.charAt(0).toLowerCase() + pureKey.slice(1, pureKey.length);
          attributes[pureKey] = normalizeData(attributes[key]);
        });

      return attributes;
    },

    getDataAttribute(element, key) {
      return normalizeData(element.getAttribute(`data-mdb-${normalizeDataKey(key)}`));
    },

    offset(element) {
      const rect = element.getBoundingClientRect();

      return {
        top: rect.top + document.body.scrollTop,
        left: rect.left + document.body.scrollLeft,
      };
    },

    position(element) {
      return {
        top: element.offsetTop,
        left: element.offsetLeft,
      };
    },

    style(element, style) {
      Object.assign(element.style, style);
    },

    toggleClass(element, className) {
      if (!element) {
        return;
      }

      if (element.classList.contains(className)) {
        element.classList.remove(className);
      } else {
        element.classList.add(className);
      }
    },

    addClass(element, className) {
      if (element.classList.contains(className)) return;
      element.classList.add(className);
    },

    addStyle(element, style) {
      Object.keys(style).forEach((property) => {
        element.style[property] = style[property];
      });
    },

    removeClass(element, className) {
      if (!element.classList.contains(className)) return;
      element.classList.remove(className);
    },

    hasClass(element, className) {
      return element.classList.contains(className);
    },
  };


  /**
   * ------------------------------------------------------------------------
   * Import SelectorEngine Class
   * ------------------------------------------------------------------------
   */

  const CustomSelectorEngine = {
    closest(element, selector) {
      return element.closest(selector);
    },

    matches(element, selector) {
      return element.matches(selector);
    },

    find(selector, element = document.documentElement) {
      return [].concat(...Element.prototype.querySelectorAll.call(element, selector));
    },

    findOne(selector, element = document.documentElement) {
      return Element.prototype.querySelector.call(element, selector);
    },

    children(element, selector) {
      const children = [].concat(...element.children);

      return children.filter((child) => child.matches(selector));
    },

    parents(element, selector) {
      const parents = [];

      let ancestor = element.parentNode;

      while (ancestor && ancestor.nodeType === Node.ELEMENT_NODE && ancestor.nodeType !== NODE_TEXT) {
        if (this.matches(ancestor, selector)) {
          parents.push(ancestor);
        }

        ancestor = ancestor.parentNode;
      }

      return parents;
    },

    prev(element, selector) {
      let previous = element.previousElementSibling;

      while (previous) {
        if (previous.matches(selector)) {
          return [previous];
        }

        previous = previous.previousElementSibling;
      }

      return [];
    },

    next(element, selector) {
      let next = element.nextElementSibling;

      while (next) {
        if (this.matches(next, selector)) {
          return [next];
        }

        next = next.nextElementSibling;
      }

      return [];
    },
  };

  /**
   * ------------------------------------------------------------------------
   * Constants
   * ------------------------------------------------------------------------
   */

  const NAME$i = 'input';
  const DATA_KEY$i = 'bs.input';
  const CLASSNAME_WRAPPER$i = 'form-outline';
  const CLASSNAME_ACTIVE$i = 'active';
  const CLASSNAME_NOTCH$i = 'form-notch';
  const CLASSNAME_NOTCH_LEADING$i = 'form-notch-leading';
  const CLASSNAME_NOTCH_MIDDLE$i = 'form-notch-middle';
  const CLASSNAME_NOTCH_TRAILING$i = 'form-notch-trailing';
  const CLASSNAME_PLACEHOLDER_ACTIVE$i = 'placeholder-active';
  const CLASSNAME_HELPER$i = 'form-helper';
  const CLASSNAME_COUNTER$i = 'form-counter';

  const SELECTOR_OUTLINE_INPUT$i = `.${CLASSNAME_WRAPPER$i} input`;
  const SELECTOR_OUTLINE_TEXTAREA$i = `.${CLASSNAME_WRAPPER$i} textarea`;
  const SELECTOR_NOTCH$i = `.${CLASSNAME_NOTCH$i}`;
  const SELECTOR_NOTCH_LEADING$i = `.${CLASSNAME_NOTCH_LEADING$i}`;
  const SELECTOR_NOTCH_MIDDLE$i = `.${CLASSNAME_NOTCH_MIDDLE$i}`;
  const SELECTOR_HELPER$i = `.${CLASSNAME_HELPER$i}`;

  /**
   * ------------------------------------------------------------------------
   * Class Definition
   * ------------------------------------------------------------------------
   */

  class Input {
    constructor(element) {
      this._element = element;
      this._label = null;
      this._labelWidth = 0;
      this._labelMarginLeft = 0;
      this._notchLeading = null;
      this._notchMiddle = null;
      this._notchTrailing = null;
      this._initiated = false;
      this._helper = null;
      this._counter = false;
      this._counterElement = null;
      this._maxLength = 0;
      this._leadingIcon = null;
      if (this._element) {
        CustomData.setData(element, DATA_KEY$i, this);
        this.init();
      }
    }

    // Getters
    static get NAME() {
      return NAME$i;
    }

    get input() {
      const inputElement =
        CustomSelectorEngine.findOne('input', this._element) ||
        CustomSelectorEngine.findOne('textarea', this._element);
      return inputElement;
    }

    // Public
    init() {
      if (this._initiated) {
        return;
      }
      this._getLabelData();
      this._applyDivs();
      this._applyNotch();
      this._activate();
      this._getHelper();
      this._getCounter();
      this._initiated = true;
    }

    update() {
      this._getLabelData();
      this._getNotchData();
      this._applyNotch();
      this._activate();
      this._getHelper();
      this._getCounter();
    }

    forceActive() {
      CustomManipulator.addClass(this.input, CLASSNAME_ACTIVE$i);
    }

    forceInactive() {
      CustomManipulator.removeClass(this.input, CLASSNAME_ACTIVE$i);
    }

    dispose() {
      this._removeBorder();

      CustomData.removeData(this._element, DATA_KEY$i);
      this._element = null;f
    }

    // Private

    _getLabelData() {
      this._label = CustomSelectorEngine.findOne('label', this._element);
      if (this._label === null) {
        this._showPlaceholder();
      } else {
        this._getLabelWidth();
        this._getLabelPositionInInputGroup();
        this._toggleDefaultDatePlaceholder();
      }
    }

    _getHelper() {
      this._helper = CustomSelectorEngine.findOne(SELECTOR_HELPER$i, this._element);
    }

    _getCounter() {
      this._counter = CustomManipulator.getDataAttribute(this.input, 'showcounter');
      if (this._counter) {
        this._maxLength = this.input.maxLength;
        this._showCounter();
      }
    }

    _showCounter() {
      const counters = CustomSelectorEngine.find('.form-counter', this._element);
      if (counters.length > 0) {
        return;
      }
      this._counterElement = document.createElement('div');
      CustomManipulator.addClass(this._counterElement, CLASSNAME_COUNTER$i);
      const actualLength = this.input.value.length;
      this._counterElement.innerHTML = `${actualLength} / ${this._maxLength}`;
      this._helper.appendChild(this._counterElement);
      this._bindCounter();
    }

    _bindCounter() {
      CustomEventHandler.on(this.input, 'input', () => {
        const actualLength = this.input.value.length;
        this._counterElement.innerHTML = `${actualLength} / ${this._maxLength}`;
      });
    }

    _toggleDefaultDatePlaceholder(input = this.input) {
      const isTypeDate = input.getAttribute('type') === 'date';

      if (!isTypeDate) {
        return;
      }

      const isInputFocused = document.activeElement === input;

      if (!isInputFocused && !input.value) {
        input.style.opacity = 0;
      } else {
        input.style.opacity = 1;
      }
    }

    _showPlaceholder() {
      CustomManipulator.addClass(this.input, CLASSNAME_PLACEHOLDER_ACTIVE$i);
    }

    _getNotchData() {
      this._notchMiddle = CustomSelectorEngine.findOne(SELECTOR_NOTCH_MIDDLE$i, this._element);
      this._notchLeading = CustomSelectorEngine.findOne(SELECTOR_NOTCH_LEADING$i, this._element);
    }

    _getLabelWidth() {
      this._labelWidth = this._label.clientWidth * 0.8 + 8;
    }

    _getLabelPositionInInputGroup() {
      this._labelMarginLeft = 0;

      if (!this._element.classList.contains('input-group')) return;
      const input = this.input;
      const prefix = CustomSelectorEngine.prev(input, '.input-group-text')[0];
      if (prefix === undefined) {
        this._labelMarginLeft = 0;
      } else {
        this._labelMarginLeft = prefix.offsetWidth - 1;
      }
    }

    _applyDivs() {
      const allNotchWrappers = CustomSelectorEngine.find(SELECTOR_NOTCH$i, this._element);
      const notchWrapper = element('div');
      CustomManipulator.addClass(notchWrapper, CLASSNAME_NOTCH$i);
      this._notchLeading = element('div');
      CustomManipulator.addClass(this._notchLeading, CLASSNAME_NOTCH_LEADING$i);
      this._notchMiddle = element('div');
      CustomManipulator.addClass(this._notchMiddle, CLASSNAME_NOTCH_MIDDLE$i);
      this._notchTrailing = element('div');
      CustomManipulator.addClass(this._notchTrailing, CLASSNAME_NOTCH_TRAILING$i);
      if (allNotchWrappers.length >= 1) {
        return;
      }
      notchWrapper.append(this._notchLeading);
      notchWrapper.append(this._notchMiddle);
      notchWrapper.append(this._notchTrailing);
      this._element.append(notchWrapper);
    }

    _applyNotch() {
      this._notchMiddle.style.width = `${this._labelWidth}px`;
      this._notchLeading.style.width = `${this._labelMarginLeft + 9}px`;

      if (this._label === null) return;
      this._label.style.marginLeft = `${this._labelMarginLeft}px`;
    }

    _removeBorder() {
      const border = CustomSelectorEngine.findOne(SELECTOR_NOTCH$i, this._element);
      if (border) border.remove();
    }

    _activate(event) {
      onDOMContentLoaded(() => {
        this._getElements(event);
        const input = event ? event.target : this.input;

        if (input.value !== '') {
          CustomManipulator.addClass(input, CLASSNAME_ACTIVE$i);
        }
        this._toggleDefaultDatePlaceholder(input);
      });
    }

    _getElements(event) {
      if (event) {
        this._element = event.target.parentNode;
        this._label = CustomSelectorEngine.findOne('label', this._element);
      }

      if (event && this._label) {
        const prevLabelWidth = this._labelWidth;
        this._getLabelData();

        if (prevLabelWidth !== this._labelWidth) {
          this._notchMiddle = CustomSelectorEngine.findOne('.form-notch-middle', event.target.parentNode);
          this._notchLeading = CustomSelectorEngine.findOne(
            SELECTOR_NOTCH_LEADING$i,
            event.target.parentNode
          );
          this._applyNotch();
        }
      }
    }

    _deactivate(event) {
      const input = event ? event.target : this.input;

      if (input.value === '') {
        input.classList.remove(CLASSNAME_ACTIVE$i);
      }
      this._toggleDefaultDatePlaceholder(input);
    }

    static activate(instance) {
      return function (event) {
        instance._activate(event);
      };
    }

    static deactivate(instance) {
      return function (event) {
        instance._deactivate(event);
      };
    }

    static jQueryInterface(config, options) {
      return this.each(function () {
        let data = CustomData.getData(this, DATA_KEY$i);
        const _config = typeof config === 'object' && config;
        if (!data && /dispose/.test(config)) {
          return;
        }
        if (!data) {
          data = new Input(this, _config);
        }
        if (typeof config === 'string') {
          if (typeof data[config] === 'undefined') {
            throw new TypeError(`No method named "${config}"`);
          }
          data[config](options);
        }
      });
    }

    static getInstance(element) {
      return CustomData.getData(element, DATA_KEY$i);
    }

    static getOrCreateInstance(element, config = {}) {
      return (
        this.getInstance(element) || new this(element, typeof config === 'object' ? config : null)
      );
    }
  }

  /**
   * ------------------------------------------------------------------------
   * Data Api implementation
   * ------------------------------------------------------------------------
   */

  CustomEventHandler.on(document, 'focus', SELECTOR_OUTLINE_INPUT$i, Input.activate(new Input()));
  CustomEventHandler.on(document, 'input', SELECTOR_OUTLINE_INPUT$i, Input.activate(new Input()));
  CustomEventHandler.on(document, 'blur', SELECTOR_OUTLINE_INPUT$i, Input.deactivate(new Input()));

  CustomEventHandler.on(document, 'focus', SELECTOR_OUTLINE_TEXTAREA$i, Input.activate(new Input()));
  CustomEventHandler.on(document, 'input', SELECTOR_OUTLINE_TEXTAREA$i, Input.activate(new Input()));
  CustomEventHandler.on(document, 'blur', SELECTOR_OUTLINE_TEXTAREA$i, Input.deactivate(new Input()));

  CustomEventHandler.on(window, 'shown.bs.modal', (e) => {
    CustomSelectorEngine.find(SELECTOR_OUTLINE_INPUT$i, e.target).forEach((element) => {
      const instance = Input.getInstance(element.parentNode);
      if (!instance) {
        return;
      }
      instance.update();
    });
    CustomSelectorEngine.find(SELECTOR_OUTLINE_TEXTAREA$i, e.target).forEach((element) => {
      const instance = Input.getInstance(element.parentNode);
      if (!instance) {
        return;
      }
      instance.update();
    });
  });

  CustomEventHandler.on(window, 'shown.bs.dropdown', (e) => {
    const target = e.target.parentNode.querySelector('.dropdown-menu');
    if (target) {
      CustomSelectorEngine.find(SELECTOR_OUTLINE_INPUT$i, target).forEach((element) => {
        const instance = Input.getInstance(element.parentNode);
        if (!instance) {
          return;
        }
        instance.update();
      });
      CustomSelectorEngine.find(SELECTOR_OUTLINE_TEXTAREA$i, target).forEach((element) => {
        const instance = Input.getInstance(element.parentNode);
        if (!instance) {
          return;
        }
        instance.update();
      });
    }
  });

  CustomEventHandler.on(window, 'shown.bs.tab', (e) => {
    let targetId;

    if (e.target.href) {
      targetId = e.target.href.split('#')[1];
    } else {
      targetId = CustomManipulator.getDataAttribute(e.target, 'target').split('#')[1];
    }

    const target = CustomSelectorEngine.findOne(`#${targetId}`);
    CustomSelectorEngine.find(SELECTOR_OUTLINE_INPUT$i, target).forEach((element) => {
      const instance = Input.getInstance(element.parentNode);
      if (!instance) {
        return;
      }
      instance.update();
    });
    CustomSelectorEngine.find(SELECTOR_OUTLINE_TEXTAREA$i, target).forEach((element) => {
      const instance = Input.getInstance(element.parentNode);
      if (!instance) {
        return;
      }
      instance.update();
    });
  });

  // auto-init
  CustomSelectorEngine.find(`.${CLASSNAME_WRAPPER$i}`).map((element) => new Input(element));

  // form reset handler
  CustomEventHandler.on(window, 'reset', (e) => {
    CustomSelectorEngine.find(SELECTOR_OUTLINE_INPUT$i, e.target).forEach((element) => {
      const instance = Input.getInstance(element.parentNode);
      if (!instance) {
        return;
      }
      instance.forceInactive();
    });
    CustomSelectorEngine.find(SELECTOR_OUTLINE_TEXTAREA$i, e.target).forEach((element) => {
      const instance = Input.getInstance(element.parentNode);
      if (!instance) {
        return;
      }
      instance.forceInactive();
    });
  });

  // auto-fill
  CustomEventHandler.on(window, 'onautocomplete', (e) => {
    const instance = Input.getInstance(e.target.parentNode);
    if (!instance || !e.cancelable) {
      return;
    }
    instance.forceActive();
  });

  onDOMContentLoaded(() => {
    const $ = getjQuery();

    if ($) {
      const JQUERY_NO_CONFLICT = $.fn[NAME$i];
      $.fn[NAME$i] = Input.jQueryInterface;
      $.fn[NAME$i].Constructor = Input;
      $.fn[NAME$i].noConflict = () => {
        $.fn[NAME$i] = JQUERY_NO_CONFLICT;
        return Input.jQueryInterface;
      };
    }
  });


export default Input;