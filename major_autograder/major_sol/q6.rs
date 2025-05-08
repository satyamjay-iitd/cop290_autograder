/// Tasks:
/// This is a similar question to `generics.rs`. But here, you need to implement `PartialOrd` for
/// `Sortable<T: PartialOrd>` and `Ord` for generic `Sortable<T: Ord>`. `Sortable<T: PartialOrd>`
/// shall sort in the reverse order of `T`.

#[derive(PartialEq, Eq, Debug)]
pub struct Sortable<T> {
    pub value: T,
}

impl<T: PartialOrd> PartialOrd for Sortable<T> {
    fn partial_cmp(&self, other: &Sortable<T>) -> Option<std::cmp::Ordering> {
        if self.value == other.value {
            Some(std::cmp::Ordering::Equal)
        } else if self.value < other.value {
            Some(std::cmp::Ordering::Greater)
        } else {
            Some(std::cmp::Ordering::Less)
        }
    }
}

impl<T: Ord> Ord for Sortable<T> {
    fn cmp(&self, other: &Sortable<T>) -> std::cmp::Ordering {
        self.partial_cmp(other).unwrap()
    }
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
