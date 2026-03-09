from tcgdexsdk import Set, SerieResume
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import ContentSwitcher

from pokenux.components.card_explorer_breadcrumb import CardExplorerBreadcrumb
from pokenux.contents.series_content import SeriesContent
from pokenux.contents.sets_content import SetsContent
from pokenux.services.tcgdex import TcgDexService

class CardExplorerScreen(Screen):
    sdk = TcgDexService('fr')
    serie: SerieResume | None = reactive(None)
    set: Set | None = None

    breadcrumb: CardExplorerBreadcrumb = None
    content_switcher: ContentSwitcher = None
    sets_content: SetsContent = None

    def on_mount(self):
        self.breadcrumb = self.query_one(CardExplorerBreadcrumb)
        self.content_switcher = self.query_one(ContentSwitcher)
        self.sets_content = self.query_one(SetsContent)

    def compose(self) -> ComposeResult:
        yield CardExplorerBreadcrumb()
        with ContentSwitcher(initial='series-content'):
            yield SeriesContent(id='series-content')
            yield SetsContent(id='sets-content')

    def on_series_content_serie_selected(self, event: SeriesContent.SerieSelected) -> None:
        self.serie = event.serie

    def watch_serie(self):
        if self.serie:
            self.breadcrumb.serie = self.serie.name
            self.sets_content.sets = self.sdk.get_sets(self.serie.id)
            self.set = None
            self.content_switcher.current = 'sets-content'
        else:
            self.content_switcher.current = 'series-content'

    def watch_set(self):

        pass