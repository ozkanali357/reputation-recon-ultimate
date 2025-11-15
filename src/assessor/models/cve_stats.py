class CVEStats:
    def __init__(self, year_bins=None, open_count=0, critical_count=0, last_seen=None, kev_hits=0):
        self.year_bins = year_bins if year_bins is not None else []
        self.open_count = open_count
        self.critical_count = critical_count
        self.last_seen = last_seen
        self.kev_hits = kev_hits

    def add_year_bin(self, year_bin):
        self.year_bins.append(year_bin)

    def update_counts(self, open_count, critical_count):
        self.open_count += open_count
        self.critical_count += critical_count

    def set_last_seen(self, last_seen):
        self.last_seen = last_seen

    def increment_kev_hits(self):
        self.kev_hits += 1

    def to_dict(self):
        return {
            "year_bins": self.year_bins,
            "open_count": self.open_count,
            "critical_count": self.critical_count,
            "last_seen": self.last_seen,
            "kev_hits": self.kev_hits,
        }