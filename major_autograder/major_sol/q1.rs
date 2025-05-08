pub fn add_a_and_a_plus_2(mut x: Vec<i32>, a: i32) -> Vec<i32> {
    x.push(a);
    x.push(a + 2);
    x
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_add_a_and_a_plus_2() {
        let mut x = Vec::new();
        x = add_a_and_a_plus_2(x, 42);
        assert_eq!(x, [42, 44]);
    }
}
