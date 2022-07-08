(self.webpackChunk_N_E = self.webpackChunk_N_E || []).push([
    [405], {
        15738: function(e, t, n) {
            "use strict";
            n.d(t, {
                Z: function() {
                    return r
                }
            });
            var c = n(85893),
                o = n(9008),
                i = "UA-120904854-1",
                s = n(98859);
            var r = function() {
                return (0, c.jsx)("div", {
                    children: (0, c.jsxs)(o.default, {
                        children: [(0, c.jsx)("meta", {
                            name: "viewport",
                            content: "width=device-width, initial-scale=1"
                        }), (0, c.jsx)("meta", {
                            charSet: "UTF-8"
                        }), (0, c.jsx)("meta", {
                            httpEquiv: "X-UA-Compatible",
                            content: "IE=edge"
                        }), (0, c.jsx)("meta", {
                            httpEquiv: "Content-Type",
                            content: "text/html; charset=utf-8"
                        }), (0, c.jsx)("meta", {
                            name: "referrer",
                            content: "always"
                        }), (0, c.jsx)("title", {
                            children: "Boxicons : Premium web friendly icons for free"
                        }), (0, c.jsx)("meta", {
                            name: "title",
                            content: "Boxicons : Premium web friendly icons for free"
                        }), (0, c.jsx)("meta", {
                            name: "copyright",
                            content: "Boxicons"
                        }), (0, c.jsx)("meta", {
                            name: "description",
                            content: "Boxicons is a free collection of carefully crafted open source icons. Each icon is designed on a 24px grid with the material guidelines"
                        }), (0, c.jsx)("link", {
                            href: "https://unpkg.com/boxicons@" + s.q + "/css/boxicons.min.css",
                            rel: "stylesheet"
                        }), (0, c.jsx)("meta", {
                            property: "og:type",
                            content: "website"
                        }), (0, c.jsx)("meta", {
                            property: "og:description",
                            content: "Boxicons is a free collection of carefully crafted open source icons. Each icon is designed on a 24px grid with the material guidelines"
                        }), (0, c.jsx)("meta", {
                            id: "og-title",
                            property: "og:title",
                            content: "Boxicons : Premium web friendly icons for free"
                        }), (0, c.jsx)("meta", {
                            property: "og:url",
                            content: "https://boxicons.com/"
                        }), (0, c.jsx)("meta", {
                            property: "og:image",
                            content: "http://boxicons.com/static/img/og-image.png"
                        }), (0, c.jsx)("meta", {
                            property: "twitter:card",
                            content: "summary_large_image"
                        }), (0, c.jsx)("meta", {
                            property: "twitter:url",
                            content: "https://boxicons.com/"
                        }), (0, c.jsx)("meta", {
                            property: "twitter:title",
                            content: "Boxicons : Premium web friendly icons for free"
                        }), (0, c.jsx)("meta", {
                            property: "twitter:description",
                            content: "Boxicons is a free collection of carefully crafted open source icons. Each icon is designed on a 24px grid with the material guidelines"
                        }), (0, c.jsx)("meta", {
                            property: "twitter:image",
                            content: "http://boxicons.com/static/img/og-image.png"
                        }), (0, c.jsx)("meta", {
                            name: "keywords",
                            content: "boxicons,free icons,open source icons, royalty free icons,google icons, icon, line icon, sharp icon, material icons, premium icons, pixel perfect icons, open source icons, free icon set"
                        }), (0, c.jsx)("link", {
                            rel: "shortcut icon",
                            type: "image/x-icon",
                            href: "static/favicon.ico?v=13"
                        }), (0, c.jsx)("script", {
                            async: !0,
                            src: "https://www.googletagmanager.com/gtag/js?id=".concat(i)
                        }), (0, c.jsx)("script", {
                            dangerouslySetInnerHTML: {
                                __html: "\n            window.dataLayer = window.dataLayer || [];\n            function gtag(){dataLayer.push(arguments);}\n            gtag('js', new Date());\n            gtag('config', '".concat(i, "');\n          ")
                            }
                        })]
                    })
                })
            }
        },
        93205: function(e, t, n) {
            "use strict";
            n.r(t), n.d(t, {
                __N_SSG: function() {
                    return F
                },
                default: function() {
                    return B
                }
            });
            var c = n(85893),
                o = n(80018),
                i = n(83679),
                s = n.n(i),
                r = n(55253),
                a = n.n(r),
                l = n(67294);
            var d = function(e) {
                    var t = e.dark;
                    return (0, c.jsx)("div", {
                        className: t ? a().hero + " " + a().dark : a().hero,
                        children: (0, c.jsx)("div", {
                            className: a().container,
                            children: (0, c.jsxs)("div", {
                                className: a().hero_text,
                                children: [(0, c.jsx)("h1", {
                                    children: "High Quality Web Icons"
                                }), (0, c.jsx)("h3", {
                                    children: "Simple Open Source icons carefully crafted for designers & developers"
                                })]
                            })
                        })
                    })
                },
                u = n(60048),
                _ = n.n(u),
                m = n(98859),
                f = n(32272),
                x = n.n(f);
            var h = (0, n(11163).withRouter)((function(e) {
                    var t = e.router,
                        n = e.dark,
                        o = e.setSearch,
                        i = (0, l.useState)(""),
                        s = i[0],
                        r = i[1];
                    (0, l.useEffect)((function() {
                        t.isReady && t.query.query && (o(t.query.query), r(t.query.query))
                    }), [t, o]);
                    var a = (0, l.useState)(!1),
                        d = a[0],
                        u = a[1];
                    return (0, c.jsx)("div", {
                        className: n ? x().search + " " + x().dark : x().search,
                        children: (0, c.jsxs)("div", {
                            className: d ? x().focused + " " + x().search_box : x().search_box,
                            children: [(0, c.jsx)("div", {
                                className: x().search_icon,
                                children: (0, c.jsx)("i", {
                                    className: "bx bx-search"
                                })
                            }), (0, c.jsx)("div", {
                                className: x().search_input,
                                children: (0, c.jsx)("input", {
                                    onFocus: function() {
                                        return u(!0)
                                    },
                                    onBlur: function() {
                                        return u(!1)
                                    },
                                    type: "search",
                                    autoComplete: "off",
                                    onChange: function(e) {
                                        r(e.target.value), o(e.target.value), t.push({
                                            pathname: "/",
                                            query: {
                                                query: e.target.value
                                            }
                                        })
                                    },
                                    value: s,
                                    placeholder: "Search..."
                                })
                            })]
                        })
                    })
                })),
                p = n(39834);
            var g = function(e) {
                    var t = e.style,
                        n = e.setBox,
                        o = e.setIcon,
                        i = e.setCollectionModal,
                        s = e.collection,
                        r = e.dark,
                        a = e.count,
                        d = e.setStyle,
                        u = e.setSearch,
                        f = e.categories,
                        x = e.category,
                        g = e.setCategory,
                        j = f.filter((function(e) {
                            return e.id === x
                        })),
                        v = (0, l.useState)(!1),
                        y = v[0],
                        N = v[1],
                        b = (0, l.useState)(""),
                        w = b[0],
                        I = b[1],
                        k = (0, l.useState)(!1),
                        S = k[0],
                        L = k[1],
                        C = f.map((function(e, t) {
                            return (0, c.jsx)("li", {
                                className: x === e.id ? _().selected : "",
                                onClick: function() {
                                    g(e.id), N(!1), I("")
                                },
                                num: t + 1,
                                children: e.name
                            }, t + 1)
                        })),
                        E = (0, l.useRef)();
                    return (0, l.useEffect)((function() {
                        E.current.innerHTML = "";
                        var e = document.createElement("script");
                        e.id = "_carbonads_js", e.src = "//cdn.carbonads.com/carbon.js?serve=CESI55QN&placement=boxiconscom", E.current.appendChild(e)
                    }), []), (0, c.jsx)("div", {
                        className: r ? _().filter + " " + _().dark : _().filter,
                        children: (0, c.jsxs)("div", {
                            className: _().filter_container,
                            children: [(0, c.jsxs)("div", {
                                className: _().filter_top,
                                children: [(0, c.jsx)("div", {
                                    className: _().flex,
                                    children: (0, c.jsx)("div", {
                                        className: _().flex_wrap,
                                        ref: E
                                    })
                                }), (0, c.jsx)(h, {
                                    dark: r,
                                    setSearch: u
                                })]
                            }), (0, c.jsxs)("div", {
                                className: _().filter_bottom,
                                children: [(0, c.jsxs)("div", {
                                    className: _().filter_categories,
                                    children: [(0, c.jsx)("div", {
                                        onClick: function() {
                                            N(!0), I("vertical")
                                        },
                                        className: _().category_button,
                                        children: (0, c.jsxs)("div", {
                                            className: _().selected_category,
                                            children: [(0, c.jsx)("span", {
                                                children: 0 === x ? "All Categories" : j[0].name
                                            }), " ", (0, c.jsx)("i", {
                                                className: "bx bx-chevron-down bx-flip-" + w
                                            })]
                                        })
                                    }), y && (0, c.jsx)(p.default, {
                                        onOutsideClick: function() {
                                            N(!1), I("")
                                        },
                                        children: (0, c.jsx)("div", {
                                            className: _().category_list,
                                            children: (0, c.jsxs)("ul", {
                                                children: [(0, c.jsx)("li", {
                                                    className: 0 === x ? _().selected : "",
                                                    onClick: function() {
                                                        g(0), N(!1), I("")
                                                    },
                                                    children: "All Categories"
                                                }), C]
                                            })
                                        })
                                    }), " "]
                                }), s.length > 0 && (0, c.jsxs)("div", {
                                    className: _().collection,
                                    onMouseEnter: function() {
                                        return L(!0)
                                    },
                                    onMouseLeave: function() {
                                        return L(!1)
                                    },
                                    onClick: function() {
                                        i(!0), n(!1), o("")
                                    },
                                    children: [S ? (0, c.jsx)("i", {
                                        className: "bx bxs-collection"
                                    }) : (0, c.jsx)("i", {
                                        className: "bx bx-collection"
                                    }), (0, c.jsx)("div", {
                                        className: _().count,
                                        children: s.length
                                    })]
                                }), (0, c.jsxs)("div", {
                                    className: _().filter_count,
                                    children: [(0, c.jsxs)("b", {
                                        children: [a, " "]
                                    }), "of ", m.a, " icons"]
                                }), (0, c.jsx)("div", {
                                    className: _().filter_styles,
                                    children: (0, c.jsxs)("ul", {
                                        children: [(0, c.jsx)("li", {
                                            onClick: function() {
                                                return d("ALL")
                                            },
                                            className: "ALL" === t ? _().selected : "",
                                            children: "All"
                                        }), (0, c.jsx)("li", {
                                            onClick: function() {
                                                return d("REGULAR")
                                            },
                                            className: "REGULAR" === t ? _().selected : "",
                                            children: "Regular"
                                        }), (0, c.jsx)("li", {
                                            onClick: function() {
                                                return d("SOLID")
                                            },
                                            className: "SOLID" === t ? _().selected : "",
                                            children: "Solid"
                                        }), (0, c.jsx)("li", {
                                            onClick: function() {
                                                return d("LOGO")
                                            },
                                            className: "LOGO" === t ? _().selected : "",
                                            children: "Logos"
                                        })]
                                    })
                                })]
                            })]
                        })
                    })
                },
                j = n(42890),
                v = n.n(j),
                y = n(41664),
                N = n(53608),
                b = n.n(N),
                w = n(46138),
                I = n.n(w);
            var k = function(e) {
                var t = e.added,
                    n = e.addItem,
                    o = e.removeItem,
                    i = e.dark,
                    s = e.icon,
                    r = e.setBox,
                    a = e.currentIcon,
                    l = e.changeIcon,
                    d = t ? I().added : "",
                    u = i ? I().dark : "",
                    _ = a === s ? I().icon_selected : "",
                    m = I().icon_container + " " + u + " " + _ + " " + d,
                    f = t ? I().icon + " " + I().added : I().icon;
                return (0, c.jsxs)("div", {
                    className: m,
                    children: [t ? (0, c.jsx)("div", {
                        className: I().add,
                        onClick: function() {
                            return o(a)
                        },
                        title: "Remove from Collection",
                        children: (0, c.jsx)("span", {
                            className: I().minus_icon,
                            children: (0, c.jsx)("i", {
                                className: "bx bxs-minus-circle"
                            })
                        })
                    }) : (0, c.jsx)("div", {
                        className: I().add,
                        onClick: function() {
                            return n(a)
                        },
                        title: "Add to Collection",
                        children: (0, c.jsx)("span", {
                            className: I().add_icon,
                            children: (0, c.jsx)("i", {
                                className: "bx bxs-plus-circle"
                            })
                        })
                    }), (0, c.jsxs)("div", {
                        className: I().icon_select,
                        onClick: function() {
                            l(a), r(!0)
                        },
                        children: [(0, c.jsxs)("div", {
                            className: f,
                            children: ["REGULAR" === a.type_of_icon && (0, c.jsx)("i", {
                                className: "bx bx-" + a.name
                            }), "SOLID" === a.type_of_icon && (0, c.jsx)("i", {
                                className: "bx bxs-" + a.name
                            }), "LOGO" === a.type_of_icon && (0, c.jsx)("i", {
                                className: "bx bxl-" + a.name
                            })]
                        }), (0, c.jsx)("div", {
                            className: I().icon_name,
                            children: a.name
                        })]
                    })]
                })
            };
            var S = function(e) {
                var t = e.collection,
                    n = e.addItem,
                    o = e.removeItem,
                    i = e.dark,
                    s = e.icon,
                    r = e.setBox,
                    a = e.icons,
                    d = e.changeIcon,
                    u = e.setCount,
                    _ = e.style,
                    m = e.search,
                    f = e.category,
                    x = a.filter((function(e) {
                        if (0 === f) {
                            if ("ALL" === _ && (e.name.replace("-", " ").includes(m.toLowerCase()) || e.term.find((function(e) {
                                    return e.includes(m.toLowerCase())
                                })))) return !0;
                            if ("ALL" != _ && e.type_of_icon === _ && (e.name.replace("-", " ").includes(m.toLowerCase()) || e.term.find((function(e) {
                                    return e.includes(m.toLowerCase())
                                })))) return !0
                        }
                        if (0 != f) {
                            if (f === e.category_id && "ALL" === _ && (e.name.replace("-", " ").includes(m.toLowerCase()) || e.term.find((function(e) {
                                    return e.includes(m.toLowerCase())
                                })))) return !0;
                            if (f === e.category_id && "ALL" != _ && e.type_of_icon === _ && (e.name.replace("-", " ").includes(m.toLowerCase()) || e.term.find((function(e) {
                                    return e.includes(m.toLowerCase())
                                })))) return !0
                        }
                        return !1
                    }));
                (0, l.useEffect)((function() {
                    u(x.length)
                }));
                var h = x.map((function(e, a) {
                    var l = !1;
                    return t.some((function(t) {
                        return t.slug === e.slug
                    })) && (l = !0), (0, c.jsx)(k, {
                        currentIcon: e,
                        changeIcon: d,
                        icon: s,
                        added: l,
                        addItem: n,
                        removeItem: o,
                        dark: i,
                        setBox: r,
                        num: a + 1
                    }, a + 1)
                }));
                return (0, c.jsx)("div", {
                    className: "",
                    children: 0 === x.length ? (0, c.jsxs)("div", {
                        className: b().emptymessage,
                        children: [(0, c.jsxs)("h4", {
                            children: ["No result found for '", m, "' ", "ALL" !== _ && "in " + _.toLowerCase()]
                        }), (0, c.jsxs)("p", {
                            children: ["Having trouble finding an icon, try the ", (0, c.jsx)(y.default, {
                                href: "/cheatsheet",
                                children: "Cheatsheet"
                            })]
                        })]
                    }) : (0, c.jsx)("div", {
                        className: b().icongrid,
                        children: h
                    })
                })
            };
            var L = function(e) {
                    var t = e.removeItem,
                        n = e.collection,
                        o = e.addItem,
                        i = e.dark,
                        s = e.icon,
                        r = e.setBox,
                        a = e.icons,
                        l = e.setCount,
                        d = e.changeIcon,
                        u = e.style,
                        _ = e.search,
                        m = e.category;
                    return (0, c.jsx)("div", {
                        className: v().iconlist,
                        children: (0, c.jsx)(S, {
                            collection: n,
                            addItem: o,
                            removeItem: t,
                            icon: s,
                            dark: i,
                            setBox: r,
                            setCount: l,
                            changeIcon: d,
                            search: _,
                            category: m,
                            style: u,
                            icons: a
                        })
                    })
                },
                C = n(15738),
                E = n(5152),
                H = (0, E.default)((function() {
                    return Promise.all([n.e(951), n.e(853), n.e(701)]).then(n.bind(n, 61701))
                }), {
                    loadableGenerated: {
                        webpack: function() {
                            return [61701]
                        },
                        modules: ["index.js -> ../components/home/IconBox"]
                    }
                }),
                O = (0, E.default)((function() {
                    return Promise.all([n.e(853), n.e(354), n.e(445)]).then(n.bind(n, 45445))
                }), {
                    loadableGenerated: {
                        webpack: function() {
                            return [45445]
                        },
                        modules: ["index.js -> ../components/home/Modal"]
                    }
                });
            var F = !0,
                B = function(e) {
                    var t = e.icons,
                        n = e.categories,
                        i = e.dark,
                        r = (0, l.useState)("ALL"),
                        a = r[0],
                        u = r[1],
                        _ = (0, l.useState)([]),
                        m = _[0],
                        f = _[1],
                        x = (0, l.useState)(""),
                        h = x[0],
                        p = x[1],
                        j = (0, l.useState)(0),
                        v = j[0],
                        y = j[1],
                        N = (0, l.useState)(""),
                        b = N[0],
                        w = N[1],
                        I = (0, l.useState)(24),
                        k = I[0],
                        S = I[1],
                        E = (0, l.useState)({
                            a: 1,
                            r: 0,
                            g: 0,
                            b: 0
                        }),
                        F = E[0],
                        B = E[1],
                        A = (0, l.useState)("#000000"),
                        q = A[0],
                        G = A[1],
                        T = (0, l.useState)(!1),
                        R = T[0],
                        M = T[1],
                        U = (0, l.useState)(!1),
                        P = U[0],
                        D = U[1],
                        Z = (0, l.useState)(!1),
                        X = Z[0],
                        z = Z[1],
                        Q = (0, l.useState)(t.length),
                        Y = Q[0],
                        W = Q[1],
                        J = function(e) {
                            f(m.filter((function(t) {
                                return t.slug !== e.slug
                            })))
                        },
                        K = (0, l.useState)(!1),
                        V = K[0],
                        $ = K[1],
                        ee = function() {
                            var e = window.pageYOffset;
                            $(e > 500)
                        };
                    (0, l.useEffect)((function() {
                        return window.addEventListener("scroll", ee, {
                                passive: !0
                            }), localStorage.getItem("collection") && f(JSON.parse(localStorage.getItem("collection"))),
                            function() {
                                window.removeEventListener("scroll", ee)
                            }
                    }), []), (0, l.useEffect)((function() {
                        localStorage.setItem("collection", JSON.stringify(m))
                    }), [m]);
                    var te = function(e) {
                        w(e);
                        var n = "",
                            c = !1;
                        "LOGO" !== e.type_of_icon ? "REGULAR" === e.type_of_icon ? (n = e.name + "-solid", c = t.some((function(e) {
                            return e.slug === n
                        })), D(c)) : "SOLID" === e.type_of_icon && (n = e.name + "-regular", c = t.some((function(e) {
                            return e.slug === n
                        })), D(c)) : D(!1)
                    };
                    return (0, c.jsxs)("div", {
                        className: s().container,
                        children: [(0, c.jsx)(C.Z, {}), (0, c.jsxs)("main", {
                            className: i ? s().main + " " + s().dark : s().main,
                            children: [R && (0, c.jsx)(O, {
                                iconHex: q,
                                setIconHex: G,
                                iconFill: F,
                                setIconFill: B,
                                iconSize: k,
                                setIconSize: S,
                                setCollection: f,
                                setCollectionModal: M,
                                removeItem: J,
                                collection: m
                            }), (0, c.jsx)(d, {
                                dark: i
                            }), (0, c.jsx)("div", {
                                className: s().hero_filter,
                                children: (0, c.jsx)(g, {
                                    setIcon: w,
                                    setBox: z,
                                    setCollectionModal: M,
                                    collection: m,
                                    dark: i,
                                    count: Y,
                                    category: v,
                                    setCategory: y,
                                    categories: n,
                                    setSearch: p,
                                    setStyle: u,
                                    style: a
                                })
                            }), (0, c.jsx)(L, {
                                collection: m,
                                addItem: function(e) {
                                    f([].concat((0, o.Z)(m), [e]))
                                },
                                removeItem: J,
                                dark: i,
                                setBox: z,
                                icon: b,
                                setCount: W,
                                changeIcon: te,
                                icons: t,
                                category: v,
                                search: h,
                                style: a
                            }), X && (0, c.jsx)(H, {
                                iconHex: q,
                                setIconHex: G,
                                iconFill: F,
                                setIconFill: B,
                                iconSize: k,
                                setIconSize: S,
                                opposite: P,
                                setBox: z,
                                changeIcon: te,
                                icon: b,
                                icons: t
                            }), V && (0, c.jsx)("div", {
                                className: X ? s().active + " " + s().toTop : s().toTop,
                                onClick: function() {
                                    window.scrollTo({
                                        top: 0,
                                        behavior: "smooth"
                                    })
                                },
                                children: (0, c.jsx)("i", {
                                    className: "bx bxs-chevron-up"
                                })
                            })]
                        })]
                    })
                }
        },
        78581: function(e, t, n) {
            (window.__NEXT_P = window.__NEXT_P || []).push(["/", function() {
                return n(93205)
            }])
        },
        60048: function(e) {
            e.exports = {
                filter: "Filter_filter__2k1qk",
                filter_container: "Filter_filter_container__31sds",
                flex: "Filter_flex__3hsUi",
                flex_wrap: "Filter_flex_wrap__2jUEz",
                filter_bottom: "Filter_filter_bottom__2aLNp",
                filter_categories: "Filter_filter_categories__3q6p-",
                category_button: "Filter_category_button__28QIg",
                selected_category: "Filter_selected_category__1G-r6",
                category_list: "Filter_category_list__2cy3L",
                collection: "Filter_collection__3_NW2",
                count: "Filter_count__6op6c",
                filter_count: "Filter_filter_count__3HnYx",
                filter_styles: "Filter_filter_styles__2u3KN",
                selected: "Filter_selected__oX6WR",
                dark: "Filter_dark__31ZTt"
            }
        },
        32272: function(e) {
            e.exports = {
                search: "Search_search__3w4pr",
                search_box: "Search_search_box__3B4bL",
                focused: "Search_focused__1oAGk",
                search_icon: "Search_search_icon__awInQ",
                search_input: "Search_search_input__t4lg3",
                dark: "Search_dark__F4di_"
            }
        },
        55253: function(e) {
            e.exports = {
                hero: "Hero_hero__3kOK-",
                container: "Hero_container__2SY9f",
                hero_text: "Hero_hero_text__16sqm",
                dark: "Hero_dark__4NG45"
            }
        },
        46138: function(e) {
            e.exports = {
                icon_container: "Icon_icon_container__3eYxV",
                check_icon: "Icon_check_icon__2ETJi",
                minus_icon: "Icon_minus_icon__2veC3",
                icon_select: "Icon_icon_select__1iCmb",
                add: "Icon_add__2k7x4",
                icon_selected: "Icon_icon_selected__2hKZf",
                icon: "Icon_icon__3MoOD",
                added: "Icon_added__3Hae6",
                icon_name: "Icon_icon_name__1q4xW",
                dark: "Icon_dark__3lOuM"
            }
        },
        42890: function(e) {
            e.exports = {
                iconlist: "IconList_iconlist__Ua5mO"
            }
        },
        53608: function(e) {
            e.exports = {
                icongrid: "IconMap_icongrid__265y1",
                emptymessage: "IconMap_emptymessage__1IhDc"
            }
        },
        83679: function(e) {
            e.exports = {
                main: "Home_main__1Z1aG",
                toTop: "Home_toTop__1Z-uh",
                active: "Home_active__1lDxw",
                hero_filter: "Home_hero_filter__2fYg8",
                title: "Home_title__28pEg",
                description: "Home_description__3GmI3",
                code: "Home_code__2X25X",
                grid: "Home_grid__QT_Bm",
                card: "Home_card__PT3hq",
                logo: "Home_logo__3GqVp",
                dark: "Home_dark__2MqEr"
            }
        }
    },
    function(e) {
        e.O(0, [774, 403, 888, 179], (function() {
            return t = 78581, e(e.s = t);
            var t
        }));
        var t = e.O();
        _N_E = t
    }
]);