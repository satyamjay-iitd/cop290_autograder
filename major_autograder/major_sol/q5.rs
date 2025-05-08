/// Tasks:
/// Implement `PartialOrd` and `Ord` for `Sortable<String>`. Note that `Sortable<String>` should
/// give the opposite order of `String`.
///
#[derive(PartialEq, Eq, Debug)]
pub struct Sortable<T> {
    pub value: T,
}

impl PartialOrd for Sortable<u32> {
    fn partial_cmp(&self, other: &Sortable<u32>) -> Option<std::cmp::Ordering> {
        if self.value == other.value {
            Some(std::cmp::Ordering::Equal)
        } else if self.value < other.value {
            Some(std::cmp::Ordering::Less)
        } else {
            Some(std::cmp::Ordering::Greater)
        }
    }
}

impl Ord for Sortable<u32> {
    fn cmp(&self, other: &Sortable<u32>) -> std::cmp::Ordering {
        self.partial_cmp(other).unwrap()
    }
}

impl PartialOrd for Sortable<String> {
    fn partial_cmp(&self, other: &Sortable<String>) -> Option<std::cmp::Ordering> {
        if self.value == other.value {
            Some(std::cmp::Ordering::Equal)
        } else if self.value < other.value {
            Some(std::cmp::Ordering::Greater)
        } else {
            Some(std::cmp::Ordering::Less)
        }
    }
}

impl Ord for Sortable<String> {
    fn cmp(&self, other: &Sortable<String>) -> std::cmp::Ordering {
        self.partial_cmp(other).unwrap()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_i32() {
        let mut v = vec![Sortable { value: 42 }, Sortable { value: 36 }];
        v.sort();
        assert_eq!(v, vec![Sortable { value: 36 }, Sortable { value: 42 }]);
    }

    #[test]
    fn test_str() {
        let mut v = vec![
            Sortable {
                value: String::from("cards"),
            },
            Sortable {
                value: String::from("car"),
            },
            Sortable {
                value: String::from("cargo"),
            },
        ];
        v.sort();
        assert_eq!(
            v,
            vec![
                Sortable {
                    value: String::from("cargo")
                },
                Sortable {
                    value: String::from("cards")
                },
                Sortable {
                    value: String::from("car")
                }
            ]
        );
    }
}
