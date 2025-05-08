/// Tasks:
/// This is a similar question to `generics.rs`. But here, you need to implement `PartialOrd` for
/// `Sortable<T: PartialOrd>` and `Ord` for generic `Sortable<T: Ord>`. `Sortable<T: PartialOrd>`
/// shall sort in the reverse order of `T`.

#[derive(PartialEq, Eq, Debug)]
pub struct Sortable<T> {
    pub value: T,
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn test_direct() {
        let mut v = vec![
            Sortable { value: -42 },
            Sortable { value: 36 },
            Sortable { value: 12 },
        ];
        v.sort();
        assert_eq!(
            v,
            vec![
                Sortable { value: 36 },
                Sortable { value: 12 },
                Sortable { value: -42 }
            ]
        );
    }

    #[test]
    fn test_nested() {
        let mut v = vec![
            Sortable {
                value: Sortable { value: -42 },
            },
            Sortable {
                value: Sortable { value: 36 },
            },
            Sortable {
                value: Sortable { value: 12 },
            },
        ];
        v.sort();
        assert_eq!(
            v,
            vec![
                Sortable {
                    value: Sortable { value: -42 }
                },
                Sortable {
                    value: Sortable { value: 12 }
                },
                Sortable {
                    value: Sortable { value: 36 }
                }
            ]
        );
    }

    #[test]
    fn test_3nested() {
        let mut v = vec![
            Sortable {
                value: Sortable {
                    value: Sortable { value: -42 },
                },
            },
            Sortable {
                value: Sortable {
                    value: Sortable { value: 36 },
                },
            },
            Sortable {
                value: Sortable {
                    value: Sortable { value: 12 },
                },
            },
        ];
        v.sort();
        assert_eq!(
            v,
            vec![
                Sortable {
                    value: Sortable {
                        value: Sortable { value: 36 }
                    }
                },
                Sortable {
                    value: Sortable {
                        value: Sortable { value: 12 }
                    }
                },
                Sortable {
                    value: Sortable {
                        value: Sortable { value: -42 }
                    }
                }
            ]
        );
    }
}
