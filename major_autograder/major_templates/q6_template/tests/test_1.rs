mod hidden_tests {
    use template::Sortable;

    #[test]
    fn test_direct() {
        let mut v = vec![
            Sortable { value: -142 },
            Sortable { value: 136 },
            Sortable { value: 112 },
        ];
        v.sort();
        assert_eq!(
            v,
            vec![
                Sortable { value: 136 },
                Sortable { value: 112 },
                Sortable { value: -142 }
            ]
        );
    }

    #[test]
    fn test_nested() {
        let mut v = vec![
            Sortable {
                value: Sortable { value: 136 },
            },
            Sortable {
                value: Sortable { value: -142 },
            },
            Sortable {
                value: Sortable { value: 112 },
            },
        ];
        v.sort();
        assert_eq!(
            v,
            vec![
                Sortable {
                    value: Sortable { value: -142 }
                },
                Sortable {
                    value: Sortable { value: 112 }
                },
                Sortable {
                    value: Sortable { value: 136 }
                }
            ]
        );
    }

    #[test]
    fn test_3nested() {
        let mut v = vec![
            Sortable {
                value: Sortable {
                    value: Sortable { value: 136 },
                },
            },
            Sortable {
                value: Sortable {
                    value: Sortable { value: -142 },
                },
            },
            Sortable {
                value: Sortable {
                    value: Sortable { value: 112 },
                },
            },
        ];
        v.sort();
        assert_eq!(
            v,
            vec![
                Sortable {
                    value: Sortable {
                        value: Sortable { value: 136 }
                    }
                },
                Sortable {
                    value: Sortable {
                        value: Sortable { value: 112 }
                    }
                },
                Sortable {
                    value: Sortable {
                        value: Sortable { value: -142 }
                    }
                }
            ]
        );
    }
}
