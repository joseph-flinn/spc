from utils import sliding_window, is_cycle


class Rule:
    """
    The base class for all rules.
    """
    def run(
        self,
        data: list[float],
        mean: float,
        std: float,
        verbose: bool=False
    ) -> None:
        pass


class LimitRule(Rule):
    """
    The base class for the rules to detect limit breaches.

    The LimitRule uses the sliding window technique to allow for variable sized
    windows in the ControlLimitRule, WarningLimitRule, and ZoneCLimitRule.
    """
    def __init__(self, sigmas: int=3, window_size: int=1, fail_count: int=1):
        """
        Initializes the LimitRule with the required data for each of the
        subclasses.
        """
        self.sigmas = sigmas
        self.window_size = window_size
        self.fail_count = fail_count

    def run(
        self,
        data: list[float],
        mean: float,
        std: float,
        verbose: bool=False
    ) -> None:
        """
        Find the datapoints that present issues in the window_size.

        Args:
            data: A dataset of points to analyze
            mean: The computed mean of the dataset
            std: The computed standard deviation of the dataset
        """
        issues = []
        upper_limit = mean + (self.sigmas * std)
        lower_limit = mean - (self.sigmas * std)

        if verbose:
            print(f"===== {type(self).__name__} =====")
            print(f"sigmas: {self.sigmas}, window: {self.window_size}, fail_count: {self.fail_count}")
            print(f"upper limit: {upper_limit}")
            print(f"lower limit: {lower_limit}")

        last = None
        for idx, window in enumerate(
            sliding_window(data, self.window_size)
        ):
            count_above = sum([
                1 if point > upper_limit else 0
                for point in window
            ])
            count_below = sum([
                1 if point < lower_limit else 0
                for point in window
            ])
            if count_above >= self.fail_count or count_below >= self.fail_count:
                issues.append((type(self).__name__, idx + 1))

        if verbose:
            print(f"detected: {issues}")

        return issues


class ControlLimitRule(LimitRule):
    """
    Rule 1

    Detect any points that lie outside of 3 standard deviations from the mean.
    """
    def __init__(self):
        super().__init__()


class WarningLimitRule(LimitRule):
    """
    Rule 2

    Detect any set of three points where at least two are outside of 2 standard
    deviations from the mean.
    """
    def __init__(self):
        super().__init__(sigmas=2, window_size=3, fail_count=2)


class ZoneCLimitRule(LimitRule):
    """
    Rule 3

    Detect any set of five points where at least four are outside of 1 standard
    deviation from the mean.
    """
    def __init__(self):
        super().__init__(sigmas=1, window_size=5, fail_count=4)


class SingleSideConsecutiveRule(Rule):
    """
    Rule 4

    Detect any set of eight consecutive points on one side of the center
    line.
    """
    def run(
        self,
        data: list[float],
        mean: float,
        std: float,
        verbose: bool=False
    ) -> None:
        """
        Execute Rule 4.

        Args:
            data: A dataset of points to analyze
            mean: The computed mean of the dataset
            std: The computed standard deviation of the dataset
        """
        issues = []

        if verbose:
            print(f"===== {type(self).__name__} =====")

        for idx, window in enumerate(
            sliding_window(data, 8)
        ):
            if (
                (max(window) > mean and min(window) > mean)
                or (max(window) < mean and min(window) < mean)
            ):
                issues.append((type(self).__name__, idx + 1))

        if verbose:
            print(f"detected: {issues}")

        return issues


class RunRule(Rule):
    """
    Rule 5

    Detect any set of six consecutive points that either all increase or all
    decrease.
    """
    def run(
        self,
        data: list[float],
        mean: float,
        std: float,
        verbose: bool=False
    ) -> None:
        """
        Execute Rule 5.

        Args:
            data: A dataset of points to analyze
            mean: The computed mean of the dataset
            std: The computed standard deviation of the dataset
        """
        issues = []

        if verbose:
            print(f"===== {type(self).__name__} =====")

        for idx, window in enumerate(
            sliding_window(data, 6)
        ):
            if window == sorted(window) or window == sorted(window, reverse=True):
                issues.append((type(self).__name__, idx + 1))

        if verbose:
            print(f"detected: {issues}")

        return issues


class CycleRule(Rule):
    """
    Rule 7

    Detect any cyclical patterns: points alternating up and down over 14
    samples.
    """
    def run(
        self,
        data: list[float],
        mean: float,
        std: float,
        verbose: bool=False
    ) -> None:
        """
        Execute Rule 7.

        Args:
            data: A dataset of points to analyze
            mean: The computed mean of the dataset
            std: The computed standard deviation of the dataset
        """
        issues = []

        if verbose:
            print(f"===== {type(self).__name__} =====")

        last_cycle = None
        for idx, window in enumerate(
            sliding_window(data, 15)
        ):
            if is_cycle(window):
                # detects cycles larger than the window size
                if last_cycle != idx - 1:
                    issues.append((type(self).__name__, idx + 1))
                last_cycle = idx

        if verbose:
            print(f"detected: {issues}")

        return issues


class ZoneCCycleRule(Rule):
    """
    Rule 6

    Detect any cyclical patterns within 1 standard deviation from the mean.
    """
    def run(
        self,
        data: list[float],
        mean: float,
        std: float,
        verbose: bool=False
    ) -> None:
        """
        Execute Rule 6.

        Args:
            data: A dataset of points to analyze
            mean: The computed mean of the dataset
            std: The computed standard deviation of the dataset
        """
        issues = []
        upper_limit = mean + std
        lower_limit = mean - std

        if verbose:
            print(f"===== {type(self).__name__} =====")
            print(f"upper_limit: {upper_limit}")
            print(f"lower_limit: {lower_limit}")

        for idx, window in enumerate(
            sliding_window(data, 14)
        ):
            if (
                is_cycle(window)
                and min(window) > lower_limit
                and max(window) < upper_limit
            ):
                issues.append((type(self).__name__, idx + 1))

        if verbose:
            print(f"detected: {issues}")

        return issues


class MissingZoneCRule(Rule):
    """
    Rule 8.

    Detect all sets of eight consecutive points that do not include a point
    within 1 standard deviation from the mean.
    """
    def _points_in_zone_c(
        self,
        points: list[float],
        mean: float,
        std: float
    ) -> bool:
        """
        Detect if all of the points are within one standard deviation from the
        mean.
        """
        upper_limit = mean + std
        lower_limit = mean - std

        for point in points:
            if point > lower_limit and point < upper_limit:
                return True
        return False

    def run(
        self,
        data: list[float],
        mean: float,
        std: float,
        verbose: bool=False
    ) -> None:
        """
        Execute Rule 8.

        Args:
            data: A dataset of points to analyze
            mean: The computed mean of the dataset
            std: The computed standard deviation of the dataset
        """
        issues = []

        if verbose:
            print(f"===== {type(self).__name__} =====")
            print(f"upper_limit: {mean + std}")
            print(f"lower_limit: {mean - std}")

        for idx, window in enumerate(
            sliding_window(data, 8)
        ):
            if not self._points_in_zone_c(window, mean, std):
                issues.append((type(self).__name__, idx + 1))

        if verbose:
            print(f"detected: {issues}")

        return issues


class NearLimitRule(Rule):
    """
    Rule 10

    Detect any points that are within 0.25 standard deviations from the control
    limit (3 standard deviations) or the warning limit (2 stanard deviations).
    """
    def run(
        self,
        data: list[float],
        mean: float,
        std: float,
        verbose: bool=False
    ) -> None:
        """
        Execute Rule 10.

        Args:
            data: A dataset of points to analyze
            mean: The computed mean of the dataset
            std: The computed standard deviation of the dataset
        """
        issues = []
        near = 0.25
        ucl = mean + (3 * std)
        lcl = mean - (3 * std)
        uwl = mean + (2 * std)
        lwl = mean - (2 * std)

        if verbose:
            print(f"===== {type(self).__name__} =====")
            print(f"nearness: {near}")
            print(f"ucl: {ucl}\nlcl: {lcl}")
            print(f"uwl: {uwl}\nlwl: {lwl}")

        for idx, point in enumerate(data):
            if (
                (point < ucl and point > ucl - (near * std))
                or (point < uwl and point > uwl - (near * std))
                or (point > lcl and point < lcl + (near * std))
                or (point > lwl and point < lwl + (near * std))
            ):
                issues.append((type(self).__name__, idx + 1))

        if verbose:
            print(f"detected: {issues}")

        return issues


rules = [
    ControlLimitRule(),
    WarningLimitRule(),
    ZoneCLimitRule(),
    SingleSideConsecutiveRule(),
    RunRule(),
    CycleRule(),
    ZoneCCycleRule(),
    MissingZoneCRule(),
    MissingZoneCRule(),
    NearLimitRule()
]
