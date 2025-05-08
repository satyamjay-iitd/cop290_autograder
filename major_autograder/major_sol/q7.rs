/// Tasks:
/// Fix compilation issues by adding annotations on `struct`s.
/// Fix parser to return `ParserError` on incorrect input. Only valid inputs are of the form `a=42`.
/// Left-hand side should be a single character lower-case variable name from a to z. Right-hand
/// side should be i32.
///
#[derive(PartialEq, Debug)]
pub struct Assignment<'a> {
    pub name: &'a str,
    pub val: i32,
}

#[derive(PartialEq, Debug)]
pub struct ParserError;

pub fn parse(s: &str) -> Result<Assignment, ParserError> {
    let parts = s.split("=").collect::<Vec<&str>>();
    // Hint: You can get the first character of a string with `chars().next()`. For example:
    if parts.len() != 2 {
        return Err(ParserError);
    }
    if parts[0].len() != 1 {
        return Err(ParserError);
    }
    let char = parts[0].chars().next().ok_or(ParserError)?;
    if !char.is_ascii_lowercase() {
        return Err(ParserError);
    }

    Ok(Assignment {
        name: parts[0],
        val: parts[1].parse::<i32>().map_err(|_| ParserError)?,
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_correct1() {
        let c = parse("b=42");
        assert_eq!(c, Ok(Assignment { name: "b", val: 42 }));
    }

    #[test]
    fn test_correct2() {
        let c = parse("a=hello");
        assert_eq!(c, Err(ParserError));
    }

    #[test]
    fn test_incorrect1() {
        let c = parse("b=");
        assert_eq!(c, Err(ParserError));
    }

    #[test]
    fn test_incorrect2() {
        let c = parse("b=42=36");
        assert_eq!(c, Err(ParserError));
    }

    #[test]
    fn test_incorrect3() {
        let c = parse("aa=42");
        assert_eq!(c, Err(ParserError));
    }

    #[test]
    fn test_incorrect4() {
        let c = parse("A=42");
        assert_eq!(c, Err(ParserError));
    }
}
